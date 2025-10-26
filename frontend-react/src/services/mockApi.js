const MOCK_IMAGES = [
  {
    id: 'img_001',
    url: '/mock-images/a man riding a horse dada.png',
    thumbnail: '/mock-images/a man riding a horse dada.png',
    similarity: 0.95,
    name: 'a man riding a horse dada.png'
  },
  {
    id: 'img_002',
    url: '/mock-images/a man riding a horse studio ghibli.png',
    thumbnail: '/mock-images/a man riding a horse studio ghibli.png',
    similarity: 0.89,
    name: 'a man riding a horse studio ghibli.png'
  },
  {
    id: 'img_003',
    url: '/mock-images/anime.png',
    thumbnail: '/mock-images/anime.png',
    similarity: 0.84,
    name: 'anime.png'
  },
  {
    id: 'img_004',
    url: '/mock-images/cinematic.png',
    thumbnail: '/mock-images/cinematic.png',
    similarity: 0.78,
    name: 'cinematic.png'
  },
  {
    id: 'img_005',
    url: '/mock-images/pixel art.png',
    thumbnail: '/mock-images/pixel art.png',
    similarity: 0.72,
    name: 'pixel art.png'
  }
];

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export const uploadImage = async (imageFile) => {
  await delay(800);
  
  return {
    image_id: `mock_${Date.now()}`,
    status: 'success',
    filename: imageFile.name
  };
};

export const getSimilarImages = async (imageId) => {
  await delay(1200);
  
  const shuffled = [...MOCK_IMAGES].sort(() => Math.random() - 0.5);
  
  return shuffled;
};

export const uploadAndGetSimilar = async (imageFile) => {
  const uploadResult = await uploadImage(imageFile);
  const similarImages = await getSimilarImages(uploadResult.image_id);
  return similarImages;
};
