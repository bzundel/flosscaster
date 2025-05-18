//Import the style sheet for the bar section
import styles from "./bar.module.css";

//Returns the section, which acts as bar, to the function in App.jsx
export const Bar = () => {
  return (
    <section className={styles.container}>
       {/* This section is used to create a bar, with css, that separates the hero and podcast list sections */}
    </section>
  )
}