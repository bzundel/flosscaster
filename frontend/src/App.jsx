import styles from './App.css';
import { Navbar } from './components/navbar/navbar.jsx';
import { Hero } from './components/hero/hero.jsx';
import { PodcastLists } from './components/podcasts/podcastLists.jsx';
import { Published } from './components/published/published.jsx';

function App() {
  return (
    <div className={styles.app}>
      <Navbar/>,
      <Hero/>,
      <Published/>,
      <PodcastLists/>
    </div>
  );
}

export default App;
