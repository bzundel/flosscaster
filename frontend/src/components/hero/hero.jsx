import React from 'react';
import styles from "./hero.module.css";


export const Hero = () => {
  return (
      <section className={styles.container}>
        <div className={styles.content}>
          <h1 className={styles.mainHeader}> Podcasts without limits</h1>
          <p className={styles.mainParagraph}>Want to hear the newest episode?</p>
          <a href="" className={styles.heroButton} a> Hear now</a>
        </div>
        <img className={styles.mainPicture} src="./assets/hero_picture.png" alt="Hero Section"/>
        <div className={styles.topBlur} />
        <div className={styles.bottomBlur} />
      </section>
  )
}
