import React, { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("/api/list")
      .then(response => response.json())
      .then(json => setData(json));
  }, []);

  return (
    <div>
      <h1>Flosscaster Home</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default App;
