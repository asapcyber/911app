// Frontend build sometimes runs before @types/leaflet is fully resolved.
// This shim keeps TS happy if the loader stumbles.
declare module 'leaflet';
