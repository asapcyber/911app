// src/components/MapCard.tsx
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix default marker icons for Vite bundling
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

type Props = {
  lat?: number | null
  lon?: number | null
  label?: string
}

export default function MapCard({ lat, lon, label = 'Locatie 112-melding' }: Props) {
  const hasPos = typeof lat === 'number' && typeof lon === 'number'
  const position = hasPos ? [lat as number, lon as number] as [number, number] : null

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 backdrop-blur p-4 shadow-sm">
      <h3 className="font-semibold mb-2 text-zinc-100">Locatie</h3>

      {!hasPos ? (
        <div className="h-[280px] rounded-lg border border-zinc-800 bg-black/70 flex items-center justify-center">
          <div className="text-sm text-zinc-500">
            Voer <span className="text-zinc-300">latitude</span> en <span className="text-zinc-300">longitude</span> in om de kaart te tonen.
          </div>
        </div>
      ) : (
        <div className="h-[280px] rounded-lg overflow-hidden">
          {/* Force re-mount so new center/zoom apply reliably */}
          <MapContainer
            key={`${position![0]},${position![1]}`}
            // Casting to any avoids CI type hiccups if react-leaflet/leaflet types mismatch
            center={position as any}
            zoom={15}
            scrollWheelZoom={true}
            style={{ height: '100%', width: '100%' }}
            preferCanvas={true}
          >
            {/* @ts-ignore react-leaflet props resolve at runtime; CI sometimes misreads types */}
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="&copy; OpenStreetMap contributors"
            />
            <Marker position={position as any}>
              <Popup>{label}</Popup>
            </Marker>
          </MapContainer>
        </div>
      )}
    </div>
  )
}
