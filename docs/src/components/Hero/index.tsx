import React, { useEffect, useState } from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './styles.module.css';

const features = [
  {
    icon: '🤖',
    title: 'Humanoid Robotics',
    description: 'Learn to build intelligent humanoid robots from scratch',
  },
  {
    icon: '🧠',
    title: 'Physical AI',
    description: 'Integrate AI with physical systems and real-world environments',
  },
  {
    icon: '⚙️',
    title: 'ROS 2 & Isaac Sim',
    description: 'Master modern robotics frameworks and simulation tools',
  },
  {
    icon: '💡',
    title: 'AI-Powered Chat',
    description: 'Get instant answers from our intelligent documentation assistant',
  },
];

export default function Hero(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  return (
    <header className={`${styles.heroBanner} ${isVisible ? styles.visible : ''}`}>
      <div className={styles.heroContainer}>
        {/* Animated Background */}
        <div className={styles.heroBackground}>
          <div className={styles.gradientOrb1}></div>
          <div className={styles.gradientOrb2}></div>
          <div className={styles.gradientOrb3}></div>
        </div>

        {/* Hero Content */}
        <div className={styles.heroContent}>
          <div className={styles.heroText}>
            <div className={styles.badge}>
              <span className={styles.badgeIcon}>✨</span>
              <span>Comprehensive Guide to Modern Robotics</span>
            </div>

            <h1 className={styles.heroTitle}>
              {siteConfig.title}
            </h1>

            <p className={styles.heroSubtitle}>
              {siteConfig.tagline}
            </p>

            <div className={styles.heroButtons}>
              <Link
                className={`button button--primary button--lg ${styles.buttonPrimary}`}
                to="/docs/intro">
                Start Learning 📚
              </Link>
              <Link
                className={`button button--secondary button--lg ${styles.buttonSecondary}`}
                href="https://github.com/Tariq6610/Physical-Ai-and-Humanoid-Robotics"
                target="_blank"
                rel="noopener noreferrer">
                View on GitHub →
              </Link>
            </div>
          </div>
        </div>

        {/* Feature Cards */}
        <div className={styles.features}>
          {features.map((feature, idx) => (
            <div
              key={idx}
              className={styles.featureCard}
              style={{animationDelay: `${idx * 100}ms`}}
            >
              <div className={styles.featureIcon}>{feature.icon}</div>
              <h3 className={styles.featureTitle}>{feature.title}</h3>
              <p className={styles.featureDescription}>{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </header>
  );
}
