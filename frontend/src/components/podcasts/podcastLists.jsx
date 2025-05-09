import styles from './podcastLists.module.css';
import React, { useState, useEffect, useRef } from 'react'

export const PodcastLists = () => {

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const fileInputRef = useRef(null);
  const [episodes, setEpisodes] = useState([]);
  
  const[showUpload, setShowUpload] = useState(false);
  const handleOpen = () => setShowUpload(true);
  const handleClose = () => setShowUpload(false);
  
  const handleSumbit =async (e) => {
    e.preventDefault();
    
    const selectedFile = fileInputRef.current?.files[0];
    if (!title || !description|| !selectedFile) {
      alert("Please fill all fields and choose a file.");
      return;
    }
    
    const formData = new FormData();
    formData.append("title", title);
    formData.append("description", description);
    formData.append("audio", selectedFile);

    try{
      const response = await fetch("http://localhost:1111/api/create",{
        method: "POST",
        body: formData,
      });
      
      if(response.ok){
        alert("Upload successful!");
        setTitle("");
        setDescription("");
        fileInputRef.current.value = null;
        setShowUpload(false);
        fetchEpisodes();
      } else{
        alert("Upload failed");
      }
    } catch(err){
      console.error("Error", err);
      alert("Server error");
    }
  };
  
  const fetchEpisodes = async () => {
    const response = await fetch("http://localhost:1111/api/list");
    const data = await response.json();
    setEpisodes(data.reverse()); // Show newest first
  };
  
  useEffect(() => {
    fetchEpisodes();
  }, []);
  
  return (
    <section className={styles.container}>
        <h1 className={styles.mainHeader}>Latest Episodes</h1>
        <button onClick={handleOpen}className={styles.showUploadBtn}>
          Upload Episode
          </button>
      
          {showUpload && (
            <div className={styles.topContainer}> 
            <div className={styles.top}>
              <h3>File Upload</h3>
              <form onSubmit={handleSumbit}>
                <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Enter Podcast Title"></input>
                <input type="text" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Enter Podcast Description"></input>
                <input type="file" accept="audio/mpeg" ref={fileInputRef}/>
              <button type="submit" name="submit" className={styles.submit}>Submit</button>
              </form>
              <span onClick={handleClose} className={styles.close}>&times;</span> {/* &times stands for the X on the right corner of the form with class close*/}
            </div>
          </div>
          )}
      <div className={styles.episodeList}>
        {episodes.map((ep) => (
          <div className={styles.podcastCard} key={ep.id}>
            <h3 className={styles.podcastTitle}>{ep.title}</h3>
            <p className={styles.podcastDescription}>{ep.description}</p>
            {ep.filepath && (
              <audio controls>
                <source src={`http://localhost:1111/uploads/${ep.filepath}`} type="audio/mp3" />
                Your browser does not support the audio element.
              </audio>
            )}
          </div>
        ))}
      </div>
      </section>
  )
}