"use client";

import React, { useState } from "react";
import { Form, Input, Button, Typography, Collapse, Tabs, Card, Tag, Badge, Space } from "antd";

type Course = {
  courseID: string;
  name: string;
  credit_hours: number;
  hub_credits: string[];
  is_major_requirement: boolean;
  major_group?: string;
  notes?: string;
};

type Semester = {
  year: number;
  semester: string;
  courses: Course[];
  semester_credits: number;
};

type CourseData = {
  degree: string;
  college: string;
  total_credits: number;
  schedule: Semester[];
  summary: {
    total_cs_major_courses: number;
    total_credits_breakdown: {
      cs_major: number;
      related_requirements: number;
      hub_requirements: number;
      total: number;
    };
  };
};

function CourseCard({ course }: { course: Course }) {
  return (
    <Card
      size="small"
      title={
        <Space>
          {course.courseID}
          {course.is_major_requirement && (
            <Badge status="processing" text={<Tag color="blue">Major Requirement</Tag>} />
          )}
        </Space>
      }
      style={{
        marginBottom: 16,
        borderLeft: course.is_major_requirement ? "4px solid #1890ff" : undefined,
      }}
    >
      <Typography.Text strong>{course.name}</Typography.Text>
      <div style={{ marginTop: 8 }}>
        <Space wrap>
          <Tag color="green">{course.credit_hours} credits</Tag>
          {course.major_group && <Tag color="purple">{course.major_group}</Tag>}
          {course.hub_credits.map((credit, index) => (
            <Tag key={index} color="orange">{credit}</Tag>
          ))}
        </Space>
      </div>
      {course.notes && (
        <Typography.Text type="secondary" style={{ display: "block", marginTop: 8 }}>
          Note: {course.notes}
        </Typography.Text>
      )}
    </Card>
  );
}

function SemesterPanel({ semester }: { semester: Semester }) {
  return (
    <div>
      <Typography.Title level={5} style={{ marginTop: 16 }}>
        {semester.semester} Semester ({semester.semester_credits} credits)
      </Typography.Title>
      {semester.courses.map((course, index) => (
        <CourseCard key={index} course={course} />
      ))}
    </div>
  );
}

function YearPanel({ yearData }: { yearData: Semester[] }) {
  const items = yearData.map((semester) => ({
    key: semester.semester,
    label: semester.semester,
    children: <SemesterPanel semester={semester} />,
  }));

  return <Tabs items={items} />;
}

export default function Home() {
  const [submitted, setSubmitted] = useState<null | { major: string; career: string }>(null);
  const [courses, setCourses] = useState<CourseData | null>(null);

  const onFinish = async (values: { major: string; career: string }) => {
    try {
      setSubmitted(values);
      const response = await fetch('/api/courses');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setCourses(data);
    } catch (error) {
      console.error('Error fetching course data:', error);
    }
  };

  // Group semesters by year
  const yearGroups = courses?.schedule.reduce((groups, semester) => {
    const year = semester.year;
    if (!groups[year]) {
      groups[year] = [];
    }
    groups[year].push(semester);
    return groups;
  }, {} as Record<number, Semester[]>) || {};

  const yearPanels = Object.entries(yearGroups).map(([year, semesters]) => ({
    key: year,
    label: `Year ${year}`,
    children: <YearPanel yearData={semesters} />,
  }));

  return (
    <div style={{ maxWidth: 1200, margin: "40px auto", padding: "0 16px" }}>
      <Typography.Title level={1}>Welcome to BU Course Planner!</Typography.Title>

      <Form layout="vertical" onFinish={onFinish}>
        <Form.Item
          label="Major"
          name="major"
          rules={[{ required: true, message: "Please enter your major" }]}
        >
          <Input placeholder="Enter major here..." />
        </Form.Item>

        <Form.Item
          label="Career"
          name="career"
          rules={[{ required: true, message: "Please enter your desired career" }]}
        >
          <Input placeholder="Enter desired career here..." />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit">
            Create Plan
          </Button>
        </Form.Item>
      </Form>

      {submitted && courses && (
        <div style={{ marginTop: 28 }}>
          <Space direction="vertical" style={{ width: "100%" }}>
            <Card>
              <Typography.Title level={4}>Program Overview</Typography.Title>
              <Space wrap>
                <Tag color="blue">{courses.degree}</Tag>
                <Tag color="cyan">{courses.college}</Tag>
                <Tag color="green">Total Credits: {courses.total_credits}</Tag>
                <Tag color="purple">Major Credits: {courses.summary.total_credits_breakdown.cs_major}</Tag>
              </Space>
            </Card>

            <Collapse
              defaultActiveKey={["1"]}
              items={yearPanels}
              style={{ background: "white" }}
            />
          </Space>
        </div>
      )}
    </div>
  );
}
