import React from 'react';
import styles from './navbar.module.css';

export const Navbar = () => {
  return (
      <section>
        <div className={styles.navbar}>
          <a href="/" className={styles.mainHeader}>Flosscaster</a>
        </div>
      </section>
  )
}
