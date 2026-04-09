import React, { useState, useRef, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  FlatList,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import HeaderForum from "../components/HeaderForum";
import FooterForum from "../components/FooterForum";

export default function ConversaScreen({ route }) {
  const topico = route?.params?.topico || "Fórum";
  const usuarioAtual = "Você";

  const flatListRef = useRef();

  const [mensagens, setMensagens] = useState([
    { id: "1", usuario: "Ana", texto: "Alguém já usou React Native?" },
    { id: "2", usuario: "Carlos", texto: "Sim! É muito bom 🔥" },
    { id: "3", usuario: "Você", texto: "Tô aprendendo agora!" },
  ]);

  const [novaMensagem, setNovaMensagem] = useState("");

  const enviarMensagem = () => {
    if (novaMensagem.trim() !== "") {
      const nova = {
        id: Date.now().toString(),
        usuario: usuarioAtual,
        texto: novaMensagem,
      };

      setMensagens((prev) => [...prev, nova]);
      setNovaMensagem("");
    }
  };

  // 🔥 scroll automático
  useEffect(() => {
    flatListRef.current?.scrollToEnd({ animated: true });
  }, [mensagens]);

  const renderItem = ({ item }) => {
    const ehUsuario = item.usuario === usuarioAtual;

    return (
      <View
      
        style={[
          styles.mensagemContainer,
          ehUsuario ? styles.direita : styles.esquerda,
        ]}
      >
        {!ehUsuario && (
          <Text style={styles.nomeUsuario}>{item.usuario}</Text>
        )}

        <View
          style={[
            styles.bolha,
            ehUsuario ? styles.bolhaUsuario : styles.bolhaOutros,
          ]}
        >
          <Text
            style={[
              styles.texto,
              ehUsuario && { color: "#fff" },
            ]}
          >
            {item.texto}
          </Text>
        </View>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <HeaderForum titulo={topico} />
      
      {/* 🔥 TÓPICO DISCRETO */}
      <Text style={styles.topico}>{topico}</Text>

      {/* 💬 LISTA */}
      <FlatList
        ref={flatListRef}
        data={mensagens}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        contentContainerStyle={{
          padding: 15,
          paddingBottom: 120,
        }}
      />

      {/* ✍️ INPUT BONITO */}
      <View style={styles.inputContainer}>
        <TextInput
          value={novaMensagem}
          onChangeText={setNovaMensagem}
          placeholder="Digite sua mensagem..."
          style={styles.input}
        />

        <TouchableOpacity style={styles.botao} onPress={enviarMensagem}>
          <Ionicons name="send" size={20} color="#fff" />
        </TouchableOpacity>
      </View>

      <FooterForum />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#eaeef3",
  },

  topico: {
    textAlign: "center",
    marginTop: 10,
    fontSize: 14,
    color: "#666",
  },

  mensagemContainer: {
    marginBottom: 12,
    maxWidth: "80%",
  },

  esquerda: {
    alignSelf: "flex-start",
  },

  direita: {
    alignSelf: "flex-end",
  },

  nomeUsuario: {
    fontSize: 11,
    color: "#888",
    marginBottom: 3,
  },

  bolha: {
    padding: 12,
    borderRadius: 15,
  },

  bolhaUsuario: {
    backgroundColor: "#1e4f8a",
    borderBottomRightRadius: 0,
  },

  bolhaOutros: {
    backgroundColor: "#fff",
    borderBottomLeftRadius: 0,
  },

  texto: {
    fontSize: 14,
  },

  inputContainer: {
    position: "absolute",
    bottom: 70,
    flexDirection: "row",
    alignItems: "center",
    padding: 10,
    width: "100%",
    backgroundColor: "#fff",
    borderTopWidth: 1,
    borderColor: "#ddd",
  },

  input: {
    flex: 1,
    backgroundColor: "#f2f2f2",
    borderRadius: 20,
    paddingHorizontal: 15,
    height: 40,
    marginRight: 10,
  },

  botao: {
    backgroundColor: "#187cf6",
    padding: 10,
    borderRadius: 50,
  },
});