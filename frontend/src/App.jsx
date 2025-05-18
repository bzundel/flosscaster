//Import the style sheet for the application and the jsx files of the components
import styles from './App.css';
import { Navbar } from './components/navbar/navbar.jsx';
import { Hero } from './components/hero/hero.jsx';
import { PodcastLists } from './components/podcasts/podcastLists.jsx';
import { Bar } from './components/bar/bar.jsx';

// The main App component, which acts as the root of the application.
function App() {
  // Return renders the components on the screen.
  return (
    // The main container as div for the entire application.
    <div className={styles.app}>
      {/* Renders all the following components */}
      <Navbar/>
      <Hero/>
      <Bar/>
      <PodcastLists/>
    </div>
  );
}
// Exports the App component for the main index.js file.
export default App;
