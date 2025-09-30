import React, { useState } from "react";
import './App.css';
import Hero from "./components/Hero";
import Features from "./components/Features";
import Curriculum from "./components/Curriculum";
import Pricing from "./components/Pricing";
import Testimonials from "./components/Testimonials";
import Footer from "./components/Footer";
import Navbar from "./components/Navbar";

function App() {
  const [currentView, setCurrentView] = useState("home");

  const renderCurrentView = () => {
    switch(currentView) {
      case "home":
        return (
          <>
            <Hero />
            <Features />
            <Curriculum />
            <Pricing />
            <Testimonials />
          </>
        );
      case "about":
        return <div className="container" style={{padding: '4rem 0'}}>About Page - Coming Soon</div>;
      case "contact":
        return <div className="container" style={{padding: '4rem 0'}}>Contact Page - Coming Soon</div>;
      default:
        return (
          <>
            <Hero />
            <Features />
            <Curriculum />
            <Pricing />
            <Testimonials />
          </>
        );
    }
  };

  return (
    <div className="App">
      <Navbar currentView={currentView} setCurrentView={setCurrentView} />
      <main className="main-content">
        {renderCurrentView()}
      </main>
      <Footer />
    </div>
  );
}

export default App;
