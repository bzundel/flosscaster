import styles from './podcastLists.module.css';
import React from 'react'

const podcastData = [
    {
      title: "The Story of Android",
      description: "A deep dive into Android",
      image: "./assets/logos/android.jpg",
      link: ""
    },
    {
      title: "Why iOS is better",
      description: "Explanation of iOS and the system ",
      image: "./assets/logos/iOS.jpg",
      link: ""
    },
    {
      title: "The Goat of all",
      description: "Exploring linux",
      image: "./assets/logos/linux.jpg",
      link: ""
    },
  ];

export const PodcastLists = () => {
  return (
    <section className={styles.container}>
        <h1 className={styles.mainHeader}>Latest Episodes</h1>
            {podcastData.map((podcast, index) => (
                <div key={index} className={styles.podcastCard}>
                    <img src={podcast.image} alt={podcast.title} className={styles.podcastImage} />
                    <div className={styles.podcastContent}>
                        <h3 className={styles.podcastTitle}>{podcast.title}</h3>
                        <p className={styles.podcastDescription}>{podcast.description}</p>
                        <a className={styles.playButton}
                        href={podcast.link} 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        > ▶ Play Episode
                        </a>
                    </div>
                </div>  
            ))}
    </section>
  )
}