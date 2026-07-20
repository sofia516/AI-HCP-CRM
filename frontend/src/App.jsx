import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import HCPs from "./pages/HCPs";
import Interactions from "./pages/Interactions";
import AIAssistant from "./pages/AIAssistant";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/hcps" element={<HCPs />} />
          <Route path="/interactions" element={<Interactions />} />
          <Route path="/ai-assistant" element={<AIAssistant />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;