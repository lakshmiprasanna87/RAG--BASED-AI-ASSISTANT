import { useState } from "react";

function App() {
  const [language, setLanguage] = useState("English");
  const [ayurvedaType, setAyurvedaType] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) {
      alert("Please enter a question");
      return;
    }

    setLoading(true);
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question,
            language: language,
            ayurveda_type: ayurvedaType,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();

      setAnswer(data.answer || "No answer received.");

      if (data.sources) {
        setSources(data.sources);
      }
    } catch (error) {
      console.error(error);
      setAnswer(
        "Unable to connect to the backend. Please make sure the backend server is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#f4f7f5",
        padding: "40px 20px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div
        style={{
          maxWidth: "900px",
          margin: "auto",
          backgroundColor: "white",
          padding: "35px",
          borderRadius: "15px",
          boxShadow: "0 4px 15px rgba(0,0,0,0.1)",
        }}
      >
        {/* HEADER */}
        <div style={{ textAlign: "center" }}>
          <h1 style={{ marginBottom: "8px" }}>
            🌿 IP-SAKTI Sahayak
          </h1>

          <p style={{ fontSize: "18px", color: "#555" }}>
            Multilingual IP & Ayurveda Assistant
          </p>

          <p style={{ color: "#777" }}>
            Ask questions about Ayurveda, traditional knowledge
            and Intellectual Property.
          </p>
        </div>

        <hr />

        {/* LANGUAGE */}
        <div style={{ marginTop: "25px" }}>
          <label>
            <b>🌐 Select Language</b>
          </label>

          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            style={selectStyle}
          >
            <option value="English">English</option>
            <option value="Hindi">Hindi</option>
            <option value="Telugu">Telugu</option>
          </select>
        </div>

        {/* AYURVEDA TYPE */}
        <div style={{ marginTop: "20px" }}>
          <label>
            <b>🌿 Select Ayurveda</b>
          </label>

          <select
            value={ayurvedaType}
            onChange={(e) => setAyurvedaType(e.target.value)}
            style={selectStyle}
          >
            <option value="">Select Ayurveda</option>
            <option value="india">🇮🇳 India Ayurveda</option>
            <option value="international">
              🌍 International Ayurveda
            </option>
          </select>
        </div>

        {/* INDIA AYURVEDA */}
        {ayurvedaType === "india" && (
          <div style={infoBox}>
            <h3>🇮🇳 India Ayurveda</h3>
            <p>
              Explore Indian traditional knowledge, Ayurveda
              practices and related intellectual property information.
            </p>
          </div>
        )}

        {/* INTERNATIONAL AYURVEDA */}
        {ayurvedaType === "international" && (
          <div style={infoBox}>
            <h3>🌍 International Ayurveda</h3>
            <p>
              Explore Ayurveda-related knowledge and intellectual
              property information from an international perspective.
            </p>
          </div>
        )}

        {/* QUESTION */}
        <div style={{ marginTop: "25px" }}>
          <label>
            <b>💬 Ask your question</b>
          </label>

          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Example: What is Intellectual Property protection for traditional knowledge?"
            rows="5"
            style={{
              width: "100%",
              marginTop: "10px",
              padding: "14px",
              borderRadius: "8px",
              border: "1px solid #ccc",
              fontSize: "16px",
              resize: "vertical",
              boxSizing: "border-box",
            }}
          />
        </div>

        {/* ASK BUTTON */}
        <button
          onClick={askQuestion}
          disabled={loading}
          style={{
            width: "100%",
            marginTop: "20px",
            padding: "14px",
            border: "none",
            borderRadius: "8px",
            backgroundColor: "#176b45",
            color: "white",
            fontSize: "17px",
            fontWeight: "bold",
            cursor: loading ? "not-allowed" : "pointer",
          }}
        >
          {loading ? "⏳ Generating Answer..." : "🔍 Ask Question"}
        </button>

        {/* ANSWER */}
        {answer && (
          <div
            style={{
              marginTop: "30px",
              padding: "20px",
              backgroundColor: "#f1f8f4",
              borderRadius: "10px",
              border: "1px solid #d5e8dc",
            }}
          >
            <h2>🤖 Answer</h2>

            <p
              style={{
                fontSize: "16px",
                lineHeight: "1.7",
                whiteSpace: "pre-wrap",
              }}
            >
              {answer}
            </p>
          </div>
        )}

        {/* SOURCES */}
        {sources.length > 0 && (
          <div style={{ marginTop: "25px" }}>
            <h2>📚 Sources</h2>

            <ul>
              {sources.map((source, index) => (
                <li key={index} style={{ marginBottom: "10px" }}>
                  {typeof source === "string"
                    ? source
                    : source.title || source.name || JSON.stringify(source)}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* FOOTER */}
        <div
          style={{
            marginTop: "35px",
            textAlign: "center",
            color: "#777",
            fontSize: "13px",
          }}
        >
          IP-SAKTI Sahayak • Multilingual RAG Assistant
        </div>
      </div>
    </div>
  );
}

const selectStyle = {
  width: "100%",
  marginTop: "10px",
  padding: "12px",
  borderRadius: "8px",
  border: "1px solid #ccc",
  fontSize: "16px",
  backgroundColor: "white",
};

const infoBox = {
  marginTop: "20px",
  padding: "15px",
  borderRadius: "8px",
  backgroundColor: "#faf6e8",
  border: "1px solid #eadfb9",
};

export default App;