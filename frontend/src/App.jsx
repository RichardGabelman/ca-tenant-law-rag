import { useState } from "react";
import "./App.css";
import Header from "./components/Header.jsx";
import QueryInput from "./components/QueryInput.jsx";

function App() {
  const [situation, setSituation] = useState("");

  async function handleSubmit() {
    console.log("submitted! (placeholder)");
  }

  return (
    <>
      <Header />
      <QueryInput
        situation={situation}
        setSituation={setSituation}
        onSubmit={handleSubmit}
      />
    </>
  );
}

export default App;
