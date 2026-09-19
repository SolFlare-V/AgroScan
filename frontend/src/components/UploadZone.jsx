import { useState, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Leaf, Upload, X, Loader2, Image as ImageIcon, Sparkles } from 'lucide-react';

const UploadZone = ({ onResult, onLoading }) => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFile = (file) => {
    if (!file.type.startsWith('image/')) {
      setError("Please upload a valid image file.");
      return;
    }
    setError(null);
    setSelectedImage(file);
  };

  const analyzeImage = async () => {
    if (!selectedImage) return;

    setIsLoading(true);
    onLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedImage);

    try {
      const response = await axios.post('http://localhost:8000/predict', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      onResult(response.data);
    } catch (err) {
      console.error(err);
      setError("Failed to reach diagnostic server. Make sure the backend is running.");
    } finally {
      setIsLoading(false);
      onLoading(false);
    }
  };

  return (
    <div className="w-full max-w-xl mx-auto space-y-6">
      <motion.div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => !selectedImage && fileInputRef.current.click()}
        className={`relative glass-card border-2 border-dashed h-80 flex flex-col items-center justify-center transition-all cursor-pointer overflow-hidden ${
          dragActive 
            ? 'border-agro-terminal bg-agro-terminal/5 scale-[1.02]' 
            : 'border-agro-terminal/20 hover:border-agro-terminal/50 hover:bg-white/5 shadow-inner'
        }`}
        whileHover={{ scale: selectedImage ? 1 : 1.01 }}
        whileTap={{ scale: 0.99 }}
      >
        <input 
          ref={fileInputRef}
          type="file" 
          className="hidden" 
          onChange={(e) => e.target.files[0] && handleFile(e.target.files[0])}
          accept="image/*"
        />

        <AnimatePresence mode="wait">
          {!selectedImage ? (
            <motion.div 
              key="upload-prompt"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col items-center gap-4 text-center px-6"
            >
              <div className="w-16 h-16 rounded-3xl bg-agro-terminal/10 border border-agro-terminal/20 flex items-center justify-center group-hover:shadow-glow-green transition-all">
                <Leaf className="w-8 h-8 text-agro-terminal" />
              </div>
              <div>
                <p className="text-xl font-bold font-grotesk text-agro-terminal uppercase tracking-widest">Upload Sample</p>
                <p className="text-sm text-agro-text/50 font-medium mt-1">Drag and drop leaf image or click to browse</p>
              </div>
              <div className="flex gap-2 mt-2">
                <span className="text-[10px] bg-white/5 border border-white/10 px-2 py-1 rounded-md text-agro-text/40">PNG</span>
                <span className="text-[10px] bg-white/5 border border-white/10 px-2 py-1 rounded-md text-agro-text/40">JPG</span>
                <span className="text-[10px] bg-white/5 border border-white/10 px-2 py-1 rounded-md text-agro-text/40">HEIC</span>
              </div>
            </motion.div>
          ) : (
            <motion.div 
              key="preview"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="w-full h-full p-4 relative"
            >
              <img 
                src={URL.createObjectURL(selectedImage)} 
                alt="Selected Sample" 
                className="w-full h-full object-cover rounded-xl border border-agro-terminal/20"
              />
              <button 
                onClick={(e) => { e.stopPropagation(); setSelectedImage(null); onResult(null); }}
                className="absolute top-6 right-6 p-2 bg-agro-dark/90 border border-white/10 rounded-full text-agro-text/60 hover:text-agro-terminal hover:border-agro-terminal transition-all backdrop-blur-md"
              >
                <X className="w-4 h-4" />
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {error && (
        <motion.div 
          initial={{ opacity: 0, y: -10 }} 
          animate={{ opacity: 1, y: 0 }}
          className="p-3 bg-red-500/10 border border-red-500/20 rounded-lg text-red-500 text-xs text-center font-medium"
        >
          {error}
        </motion.div>
      )}

      <button
        disabled={!selectedImage || isLoading}
        onClick={analyzeImage}
        className={`w-full h-14 rounded-xl font-bold font-grotesk tracking-[0.2em] uppercase flex items-center justify-center gap-3 transition-all ${
          !selectedImage || isLoading
            ? 'bg-agro-text/5 text-agro-text/20 cursor-not-allowed border border-white/5'
            : 'bg-agro-terminal text-agro-dark hover:shadow-[0_0_25px_rgba(0,255,136,0.6)] hover:bg-agro-terminal/90 active:scale-95'
        }`}
      >
        {isLoading ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>Scanning...</span>
          </>
        ) : (
          <>
            <Sparkles className="w-5 h-5" />
            <span>Analyze Plant</span>
          </>
        )}
      </button>
    </div>
  );
};

export default UploadZone;
