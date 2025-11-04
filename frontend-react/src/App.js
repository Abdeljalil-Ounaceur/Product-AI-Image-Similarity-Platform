import React, { useState } from "react";
import Header from "./components/Header";
import UploadSection from "./components/UploadSection";
import ResultsGrid from "./components/ResultsGrid";
import Footer from "./components/Footer";
import { uploadAndGetSimilar } from './services/api';
// import { uploadAndGetSimilar } from "./services/mockApi"; // Use mock for testing

function App() {
  const [similarImages, setSimilarImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadedImageUrl, setUploadedImageUrl] = useState(null);

  const handleImageSubmit = async (imageFile) => {
    setLoading(true);
    setError(null);
    setUploadedImageUrl(URL.createObjectURL(imageFile));

    try {
      const images = await uploadAndGetSimilar(imageFile);
      setSimilarImages(images);
    } catch (err) {
      setError("Failed to process image. Please try again.");
      console.error(err);
      setSimilarImages([]);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSimilarImages([]);
    setUploadedImageUrl(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Header />

      <main className="py-8">
        <UploadSection
          onSubmit={handleImageSubmit}
          onReset={handleReset}
          hasResults={similarImages.length > 0 || loading}
          uploadedImageUrl={uploadedImageUrl}
        />

        {error && (
          <div className="max-w-4xl mx-auto px-4 mb-6">
            <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-400">
              {error}
            </div>
          </div>
        )}

        <ResultsGrid images={similarImages} loading={loading} />
      </main>

      <Footer />
    </div>
  );
}

export default App;
