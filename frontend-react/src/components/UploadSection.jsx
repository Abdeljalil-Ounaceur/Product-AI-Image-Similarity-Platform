import React, { useState } from 'react';

const UploadSection = ({ onSubmit }) => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleSubmit = () => {
    if (selectedImage) {
      onSubmit(selectedImage);
    }
  };

  return (
    <div className="upload-section">
      <h2>Upload Image</h2>
      
      <div className="upload-container">
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          className="file-input"
          id="file-input"
        />
        <label htmlFor="file-input" className="file-label">
          Choose Image
        </label>
      </div>

      {previewUrl && (
        <div className="preview-container">
          <img src={previewUrl} alt="Preview" className="preview-image" />
        </div>
      )}

      <button 
        onClick={handleSubmit} 
        disabled={!selectedImage}
        className="submit-button"
      >
        Find Similar Images
      </button>
    </div>
  );
};

export default UploadSection;
