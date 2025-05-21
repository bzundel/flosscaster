//Import the style sheet for the navbar section
import styles from './notice.module.css';

//Returns the section, which acts as navbar, to the function in App.jsx
export const Notice = () => {
  return (
    <div className={styles.notice}>
        <span>Demonstration deployment. For academic purposes only.</span>
      </div>
  )
}
