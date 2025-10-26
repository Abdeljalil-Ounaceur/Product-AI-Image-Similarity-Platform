import React, { useState } from 'react';
import UploadSection from './components/UploadSection';
import ImageList from './components/ImageList';
import { uploadAndGetSimilar } from './services/api';
// import { uploadAndGetSimilar } from './services/mockApi';
import './App.css';
import './styles/UploadSection.css';
import './styles/ImageList.css';
import './styles/ImageItem.css';


function App() {
  const [similarImages, setSimilarImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageSubmit = async (imageFile) => {
    setLoading(true);
    setError(null);

    try {
      const images = await uploadAndGetSimilar(imageFile);
      setSimilarImages(images);
    } catch (err) {
      setError('Failed to process image. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="app-container">
        <div className="left-panel">
          <UploadSection onSubmit={handleImageSubmit} />
          {error && <div className="error-message">{error}</div>}
        </div>
        <div className="right-panel">
          <ImageList images={similarImages} loading={loading} />
        </div>
      </div>
    </div>
  );
}

export default App;
