import { useState } from "react";
import axios from "axios";

function App() {
  const [task, setTask] = useState("");
  const [model, setModel] = useState("");

  const getLLM = async () => {
    const res = await axios.post("http://localhost:8000/recommend?task=" + task);
    setModel(res.data.model);
  };

  return (
    <div className="p-6">
      <input type="text" onChange={(e) => setTask(e.target.value)} className="border p-2" placeholder="Task like 'code' or 'doc'" />
      <button onClick={getLLM} className="ml-2 bg-blue-500 text-white px-4 py-2 rounded">Get Model</button>
      <p className="mt-4">Suggested LLM: {model}</p>
    </div>
  );
}
