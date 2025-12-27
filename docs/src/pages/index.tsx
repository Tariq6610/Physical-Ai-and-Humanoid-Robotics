import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Hero from '@site/src/components/Hero';
import styles from './index.module.css';

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Building intelligent robots, from code to deployment. Learn Physical AI and Humanoid Robotics with ROS 2, NVIDIA Isaac Sim, and modern AI techniques.">
      <Hero />
      <main className={styles.main}>
        {/* Additional sections can be added here later */}
      </main>
    </Layout>
  );
}
