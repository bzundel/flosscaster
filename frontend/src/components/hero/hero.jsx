//Import the style sheet for the hero section
import styles from "./hero.module.css";

//Returns the section, which acts as hero, to the function in App.jsx
export const Hero = () => {
  return (
      <section className={styles.container}>
        <div className={styles.content}>  {/* Creates a div that has a header, a paragraph and a button*/}
          <h1 className={styles.mainHeader}> Podcasts without limits</h1>
          <p className={styles.mainParagraph}>Want to hear the newest episode?</p>
          {/* The html tag "input" with the type "button", acts as a button. If clicked, it gets the id of a div in podcastLists.jsx and scrolls into that section*/}
          {/* The value is the text that is seen inside the button */}
          <input type="button" onClick={() => document.getElementById('podcastList').scrollIntoView()} className={styles.heroButton} value= "Hear now" />
        </div>
        {/* The html tag "img" displays the image that is stored in the assets directory*/}
        <img className={styles.mainPicture} src="./assets/hero_picture.png" alt="Hero Section"/>
        {/* This div is used to create a colorful blur effect behind the hero image with css */}
        <div className={styles.bottomBlur} />
      </section>
  )
}