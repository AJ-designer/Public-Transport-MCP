import React from 'react';

export default function StationCard({ station }) {
  return (
    <div className="bg-white border-4 border-purple-600 rounded-3xl p-6 mt-6">
      <h4 className="text-2xl font-black text-blue-600 uppercase mb-2 italic">
        {station.name}
      </h4>
      <div className="text-lg font-bold">
        <p className="text-purple-700"> STATUS: {station.elevatorStatus}</p>
        <p className="text-blue-500 mt-2 font-black italic">⚠️ {station.notes || 'CLEAR ROUTE'}</p>
      </div>
    </div>
  );
}