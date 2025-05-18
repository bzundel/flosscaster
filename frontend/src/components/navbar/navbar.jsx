//Import the style sheet for the navbar section
import styles from './navbar.module.css';

//Returns the section, which acts as navbar, to the function in App.jsx
export const Navbar = () => {
  return (
      <section>
        {/* Creates a div that has an a tag, which acts as the main header of the webpage, like a title*/}
        <div className={styles.navbar}>
          {/* The html tag "a" has the href (hypertext reference) "blank", which means that everytime it is clicked,
          the user will get send to the beginning of the webpage */}
          <a href="/" className={styles.mainHeader}>Flosscaster</a>
        </div>
      </section>
  )
}
