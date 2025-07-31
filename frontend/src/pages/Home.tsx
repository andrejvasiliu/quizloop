import { useEffect } from "react";
import axios from "axios";
import { API_BASE_URL } from "../config";

function Home() {
  useEffect(() => {
    talkToServer();
  }, []);

  const talkToServer = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/hello`);
      console.log("Response from server:", response.data);
    } catch (error) {
      console.error("Error talking to server:", error);
    }
  };
  return (
    <div>
      <h1>Welcome to the Home Page</h1>
      <p>This is the main page of our application.</p>
    </div>
  );
}

export default Home;
