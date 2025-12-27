/**
 * Reading Progress Indicator
 * Shows a progress bar at the top of the page as user scrolls
 */

import React, { useState, useEffect } from 'react';
import styles from './styles.module.css';

export default function ReadingProgress(): JSX.Element {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const updateProgress = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrollPercent = (scrollTop / docHeight) * 100;
      setProgress(Math.min(scrollPercent, 100));
    };

    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();

    return () => window.removeEventListener('scroll', updateProgress);
  }, []);

  return (
    <div className={styles.readingProgress}>
      <div
        className={styles.readingProgressBar}
        style={{ width: `${progress}%` }}
      />
    </div>
  );
}
