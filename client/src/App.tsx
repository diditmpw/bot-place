import React, { useState, useCallback } from 'react';
import ChatWindow from './components/ChatBot/ChatWindow';
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';

const containerStyle = {
  width: '100%',
  height: '100%'
};

const defaultCenter = {
  lat: 0,
  lng: 0
};

const App: React.FC = () => {
  const [center, setCenter] = useState(defaultCenter);
  const [map, setMap] = useState<google.maps.Map | null>(null);
  const [showMarker, setShowMarker] = useState(false);

  const onLoad = useCallback((map: google.maps.Map) => {
    setMap(map);
  }, []);

  const handleLocationSelect = (lat: number, lng: number) => {
    const newCenter = { lat, lng };
    setCenter(newCenter);
    
    if (map) {
      map.panTo(newCenter);
      map.setZoom(15);
      setShowMarker(true);
    }
  };

  return (
    <div className="app" style={{ display: 'flex', height: '100%' }}>
      <ChatWindow onLocationSelect={handleLocationSelect} />
      <div style={{ flexGrow: 1, position: 'relative' }}>
        <LoadScript 
          googleMapsApiKey={process.env.GOOGLE_MAPS_API_KEY || ''}
        >
          <GoogleMap
            mapContainerStyle={containerStyle}
            center={center}
            zoom={15}
            onLoad={onLoad}
          >
            {showMarker && <Marker position={center} />}
          </GoogleMap>
        </LoadScript>
      </div>
    </div>
  );
};

export default App;