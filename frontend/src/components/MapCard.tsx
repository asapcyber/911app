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
  /** Default center used when no lat/lon provided (Groningen) */
  defaultCenter?: [number, number]
  defaultZoom?: number
}

export default function MapCard({
  lat,
  lon,
  label = 'Locatie 112-melding',
  defaultCenter = [53.21687, 6.57393], // Groningen
  defaultZoom = 13,
}: Props) {
  const hasPos = typeof lat === 'number' && typeof lon === 'number'
  const position = hasPos ? [lat as number, lon as number] as [number, number] : defaultCenter
  const markerLabel = hasPos ? label : 'Standaardlocatie (pas aan met coördinaten)'

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900/60 backdrop-blur p-4 shadow-sm">
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-semibold text-zinc-100">Locatie</h3>
        {!hasPos && (
          <span className="text-xs text-zinc-400">
            Geen coördinaten ingevoerd — toon standaardlocatie
          </span>
        )}
      </div>

      <div className="h-[280px] rounded-lg overflow-hidden">
        {/* Force re-mount on center change for reliable recentering */}
        <MapContainer
          key={`${position[0]},${position[1]}`}
          center={position as any}
          zoom={hasPos ? 15 : defaultZoom}
          scrollWheelZoom
          style={{ height: '100%', width: '100%' }}
          preferCanvas
        >
          {/* @ts-ignore react-leaflet props resolve at runtime; CI sometimes misreads types */}
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="&copy; OpenStreetMap contributors"
          />
          <Marker position={position as any}>
            <Popup>{markerLabel}</Popup>
          </Marker>
        </MapContainer>
      </div>

      <div className="mt-2 text-xs text-zinc-400">
        {hasPos
          ? `Coördinaten: ${position[0].toFixed(5)}, ${position[1].toFixed(5)}`
          : `Standaard: ${defaultCenter[0].toFixed(5)}, ${defaultCenter[1].toFixed(5)} (Groningen)`}
      </div>
    </div>
  )
}
