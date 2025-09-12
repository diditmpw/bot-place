interface Location {
  lat: number;
  lng: number;
}

interface PlaceResponse {
  type: 'place' | 'conversation';
  name: string;
  address: string;
  location: Location;
  place_id: string;
  rating: number;
  response: string;
}

export const searchPlace = async (query: string): Promise<PlaceResponse> => {
  const response = await fetch(`${process.env.SERVER_URL}/api/places/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch place data');
  }

  return response.json();
};