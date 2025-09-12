export interface ChatMessage {
    content: string;
    sender: 'user' | 'bot';
    timestamp: Date;
}

export interface Location {
    latitude: number;
    longitude: number;
    name: string;
}