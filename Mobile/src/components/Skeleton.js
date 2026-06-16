import React, { useEffect, useRef } from "react";
import { View, Animated, StyleSheet } from "react-native";

export default function Skeleton({ width, height, borderRadius = 8, style }) {
  const opacity = useRef(new Animated.Value(0.8)).current;

  useEffect(() => {
    // Cria o efeito de pulsação suave (Fade In / Fade Out)
    Animated.loop(
      Animated.sequence([
        Animated.timing(opacity, {
          toValue: 0.7,
          duration: 600,
          useNativeDriver: true,
        }),
        Animated.timing(opacity, {
          toValue: 0.3,
          duration: 600,
          useNativeDriver: true,
        }),
      ])
    ).start();
  }, [opacity]);

  return (
    <Animated.View
      style={[
        styles.skeleton,
        {
          width: width,
          height: height,
          borderRadius: borderRadius,
          opacity: opacity,
        },
        style,
      ]}
    />
  );
}

const styles = StyleSheet.create({
  skeleton: {
    backgroundColor: "#e1e1e1", // Cor base do esqueleto (cinza claro)
  },
});