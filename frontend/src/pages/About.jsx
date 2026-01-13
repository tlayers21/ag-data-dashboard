import React from "react";
import { Link } from "react-router-dom";
import "./About.css";

function About() {
  return (
    <div className="about-page">

      {/* Project Card */}
      <div className="about-card">
        <h2>About This Project</h2>
        <p>
          This platform provides a unified, automated interface for exploring USDA
          export and supply‑demand datasets across major U.S. agricultural commodities. It brings
          Export Sales Report (ESR), Production, Supply, and Distribution (PSD), and Export Inspections data together in a clean, modern,
          interactive dashboard. The underlying ESR and PSD data was fetched using the USDA FAS Open Data Web APIs, and the export inspections data
          was parsed from past reports. All charts are automatically updated daily and accomodate for reports when they are released.
        </p>

        <p>
          To learn more about the data used throughout the site, visit this{" "}
          <Link to="/data-overview" className="about-link">
            Data Overview
          </Link>{" "}
          page.
        </p>
      </div>

      {/* Developer Card */}
      <div className="about-card">
        <h2>About Me</h2>
        <p>
          I am an undergraduate student at Virginia Tech majoring in Computer Science, with minors in Mathematics and Commodity Market Analytics.
          I am part of COINS (Commodity Investing by Students), a student-run commodity trading group that researches and trades commodities using futures-based ETFs.
          The motivation behind this project is to provide our agriculture division, as well as anyone else interested, with an easy, interactive way to access
          and analyze commodity data.
          

        </p>

        <p>
          If you have any questions, requests for additional commodities or countries, or any suggestions,
          feel free to reach out.
        </p>

        <div className="contact-info">
          <p><strong>Name:</strong> Thomas Ayers</p>
          <p><strong>Email:</strong> tlayers21@gmail.com</p>
          <p><strong>Phone:</strong> (571) 510‑5440</p>
          <p>
            <strong>LinkedIn:</strong>{" "}
            <a
              href="https://www.linkedin.com/in/thomas-l-ayers"
              target="_blank"
              rel="noopener noreferrer"
            >
              View Profile
            </a>
          </p>
        </div>
      </div>

    </div>
  );
}

export default About;