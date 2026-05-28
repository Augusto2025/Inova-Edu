import React, {
  createContext,
  useState,
} from "react";

export const ThemeContext =
  createContext();

export function ThemeProvider({
  children
}) {

  const [modoEscuro, setModoEscuro] =
    useState(false);

  // TEMA CLARO
  const lightTheme = {
  fundo: "#F5F7FA",
  card: "#FFFFFF",
  texto: "#111",
  subtexto: "#666",
  borda: "#DDD",
  input: "#ECECEC",

  azul: "#2155f3",

  textoHeader: "#FFF",
  subtextoHeader: "#DDE7FF",
};

const darkTheme = {
  fundo: "#081120",
  card: "#162235",
  texto: "#FFFFFF",
  subtexto: "#AAB4C3",
  borda: "#26374D",
  input: "#314158",

  azul: "#0D1B2E",

  textoHeader: "#FFFFFF",
  subtextoHeader: "#AAB4C3",
};
  const temaClaro = {
    fundo: "#f5f7fb",
    card: "#ffffff",
    texto: "#111111",
    subtexto: "#666666",
    borda: "#dddddd",
    input: "#f1f1f1",
    azul: "#2155f3",
  };

  // TEMA ESCURO
  const temaEscuro = {
    fundo: "#0f172a",
    card: "#1e293b",
    texto: "#ffffff",
    subtexto: "#94a3b8",
    borda: "#334155",
    input: "#334155",
    azul: "#0f172a",



  };

  return (

    <ThemeContext.Provider
      value={{
        modoEscuro,
        setModoEscuro,
        tema: modoEscuro
          ? temaEscuro
          : temaClaro,

    
      }}
    >

      {children}

    </ThemeContext.Provider>

  );
}