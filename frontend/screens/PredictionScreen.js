import React, { useEffect, useState } from 'react';
import { View, Text, Button, ActivityIndicator } from 'react-native';
import api from '../services/api';

export default function PredictionScreen() {
  const [loading, setLoading] = useState(true);
  const [prediction, setPrediction] = useState(null);
  useEffect(() => {
    (async () => {
      try {
        const res = await api.get('/cycles/prediction');
        setPrediction(res.data);
      } catch (err) {
        console.error(err);
        setPrediction(null);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <ActivityIndicator style={{marginTop:20}} />;
  if (!prediction) return <View style={{padding:16}}><Text>Not enough data to predict (need ≥2 cycles).</Text></View>;

  return (
    <View style={{padding:16}}>
      <Text style={{fontWeight:'bold'}}>Predicted start: {prediction.predictedStart}</Text>
      <Text>Window: {prediction.windowStart} — {prediction.windowEnd}</Text>
      <Text>Avg cycle length: {prediction.averageCycleLength} days (sd {prediction.sd})</Text>
    </View>
  );
}
