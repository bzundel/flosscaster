//Import the style sheet for the podcast list section
import styles from './podcastLists.module.css';
// This line imports { useState, useEffect, useRef }, which are specific tools (hooks) from React: 'react' library
// useState: Store information like text or files, React updates the webpage
// useEffect: Fetching data or manually change the webpage
// useRef: Direct element access, like get a file picked from the user
import { useState, useEffect, useRef } from 'react'

// These lines are the main part of our podcast list section.
// "export const PodcastLists": means we are creating a new component with 
// the name "PodcastLists" that can be used from other parts
export const PodcastLists = () => {

  // State for the new podcast's title, description, and the list of all episodes. At start they are empty
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [episodes, setEpisodes] = useState([]);
  
  // State to control the visibility, open and closed, of the file upload form.
  const[showUpload, setShowUpload] = useState(false);
  // Ref to directly access the file input element.
  const fileInputRef = useRef(null);

  // Functions that set to show and hide the upload form.
  const handleOpen = () => setShowUpload(true);
  const handleClose = () => setShowUpload(false);

  // Get environment variable for dev and docker compatibility or defauliting to localhost
  const BACKEND_HOST = process.env.REACT_APP_BACKEND_HOST || "localhost";

  // Handles the submission of the new podcast episode form.
  // "e": represents the "event" object, that contains information about the submission
  const handleSumbit =async (e) => {   // "async": Might perform operations that take some time (like sending a file over the internet)
    e.preventDefault(); // Prevent default form submission which reloads the page.
    
    // Get the selected audio file and store it in selectedFile
    const selectedFile = fileInputRef.current?.files[0];

    // Check if all required fields are filled.
    if (!title || !description|| !selectedFile) {
      alert("Please fill all fields and choose a file.");
      return;
    }

    // Prepare the object "formData" to send to the server, including title, description and audio file.
    const formData = new FormData();
    formData.append("title", title);
    formData.append("description", description);
    formData.append("audio", selectedFile);


    try{
      // Send the podcast data to the backend API endpoint for creation.
      const response = await fetch(`http://${BACKEND_HOST}:1111/api/create`, { // "fetch": is to make requests to a server with 
        // the url address of our backend server; "await": pauses the function here until the server responds
        method: "POST", // Use POST method to send data.
        body: formData, // Attach the object "formData" as the request body.
      });
      
      // After server responds, we check if the request was successful.
      // "response.ok": is true if the server responded with a success code
      if(response.ok){
        //If successfull, print the alert and clear the states
        alert("Upload successful!");
        setTitle("");
        setDescription("");
        fileInputRef.current.value = null; // Clear the file input field
        setShowUpload(false); // Hide the upload form
        fetchEpisodes(); // Fetch the updated list of episodes from the server so the new one appears.
      } else{
        // If the server responded but it wasn't a success, the alert is printed
        alert("Upload failed");
      }
    } catch(err){ // Handle network errors or issues connecting to the server and print it
      console.error("Error", err);
      alert("Server error");
    }
  };
  
  // Fetches(Requests) the list of podcast episodes from the backend API.
  const fetchEpisodes = async () => {
    // The server sends data as JSON
    const response = await fetch(`http://${BACKEND_HOST}:1111/api/list`); //Backend URL Address.
    const data = await response.json(); // Converts this JSON data into a JavaScript object or array.
    // Update the "episodes" with the data received from the server.
    setEpisodes(data.reverse()); // Show newest first.
  };
  
  // To fetch episodes once when the component first loads.
  useEffect(() => {
    fetchEpisodes();
  }, []);
  
  // Jsx structure that returns what the component renders on the webpage.
  return (
    <section id="podcastList" className={styles.container}>
        <h1 className={styles.mainHeader}>Latest Episodes</h1>
        <button onClick={handleOpen}className={styles.showUploadBtn}> {/* Button to open the upload form modal. */}
          Upload Episode
          </button>
          {/* If "showUpload" is true, only then render the upload form. */}
          {showUpload && (
            <div className={styles.top}> {/* Div that is a container for the upload form */}
              <h3>File Upload</h3>
              <form onSubmit={handleSumbit}> {/* Form element triggers handleSumbit after submission */}
                {/* Input and textarea for the podcast title, description and file linked to the initalized states and update them */}
                <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Enter Podcast Title"></input>
                <textarea rows="5" cols="32" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Enter Podcast Description"></textarea>
                <input type="file" accept="audio/mpeg" ref={fileInputRef}/> {/* "ref={fileInputRef}" links the input so we can access the chosen file. */}
              <button type="submit" name="submit" className={styles.submit}>Submit</button> {/* Submit button */}
              </form>
              {/* The html tag "span" is here used as a "X" icon to close the upload form. If clicked, run the function "handleClose". */}
              <span onClick={handleClose} className={styles.close}>&times;</span> {/* &times stands for the X on the right corner of the form */}
            </div>
          )}
      {/* Displaying the list of podcast episodes: "episodes": is an list of episode data from the server.
       With "map()" it goes through each item (ep) in the list */}
        {episodes.map((ep) => (
          // Each episode is rendered in a div and styled. 'key' is crucial for React lists.
          <div className={styles.podcastCard} key={ep.id}>
            <h3 className={styles.podcastTitle}>{ep.title}</h3> {/* Display episode title. */}
            <p className={styles.podcastDescription}>{ep.description}</p> {/* Display episode description. */}
            {/* If a filepath exists, then render the audio player for the episode. */}
            {ep.filepath && (
              <audio controls> {/* The html tag "audio" is a default html audio player */}
                {/* Source of the audio file, constructed from backend and episode filepath. */}
                <source src={`http://${BACKEND_HOST}:1111/api/get_upload/${ep.filepath}`} type="audio/mp3"/>
                Your browser does not support the audio element. {/* Fallback text, if audio element is not supported */}
              </audio>
            )}
          </div>
        ))}
      </section>
  )
}