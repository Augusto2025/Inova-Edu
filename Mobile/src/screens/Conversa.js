import React, { useState, useRef, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  FlatList,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import Header from '../components/Header';



export default function ConversaScreen({ route }) {
  const topico = route?.params?.topico || "";
  const usuarioAtual = "Você";

  const flatListRef = useRef();

  const [mensagens, setMensagens] = useState([
    {
      id: "1",
      usuario: "Ana",
      texto: "Alguém já usou React Native?",
      hora: new Date(),
    },
    {
      id: "2",
      usuario: "Carlos",
      texto: "Sim! É muito bom 🔥",
      hora: new Date(),
    },
    {
      id: "3",
      usuario: "Você",
      texto: "Tô aprendendo agora!",
      hora: new Date(),
    },
  ]);

  const [novaMensagem, setNovaMensagem] = useState("");
  const [editandoId, setEditandoId] = useState(null);

  // ⏰ Hora
  const formatarHora = (data) => {
    return data.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  // 📅 Data estilo WhatsApp
  const formatarData = (data) => {
    const hoje = new Date();
    const ontem = new Date();
    ontem.setDate(hoje.getDate() - 1);

    const mesmaData = (d1, d2) =>
      d1.toDateString() === d2.toDateString();

    if (mesmaData(data, hoje)) return "Hoje";
    if (mesmaData(data, ontem)) return "Ontem";

    return data.toLocaleDateString("pt-BR");
  };

  const enviarMensagem = () => {
    if (novaMensagem.trim() !== "") {
      if (editandoId) {
        // ✏️ EDITAR
        setMensagens((prev) =>
          prev.map((msg) =>
            msg.id === editandoId
              ? { ...msg, texto: novaMensagem }
              : msg
          )
        );

        setEditandoId(null);
        setNovaMensagem("");
      } else {
        // 💬 NOVA
        const nova = {
          id: Date.now().toString(),
          usuario: usuarioAtual,
          texto: novaMensagem,
          hora: new Date(),
        };

        setMensagens((prev) => [...prev, nova]);
        setNovaMensagem("");
      }
    }
  };

  const excluirMensagem = (id) => {
    setMensagens((prev) => prev.filter((msg) => msg.id !== id));
  };

  const editarMensagem = (id, textoAtual) => {
    setNovaMensagem(textoAtual);
    setEditandoId(id);
  };

  const abrirMenu = (item) => {
    Alert.alert("Opções", "O que deseja fazer?", [
      {
        text: "Editar",
        onPress: () => editarMensagem(item.id, item.texto),
      },
      {
        text: "Excluir",
        onPress: () => excluirMensagem(item.id),
        style: "destructive",
      },
      { text: "Cancelar", style: "cancel" },
    ]);
  };

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

        <View style={{ flexDirection: "row", alignItems: "flex-end" }}>
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

            {/* ⏰ Hora */}
            <Text
              style={[
                styles.hora,
                ehUsuario && { color: "#ddd" },
              ]}
            >
              {formatarHora(item.hora)}
            </Text>
          </View>

          {/* ⋮ MENU */}
          {ehUsuario && (
            <TouchableOpacity onPress={() => abrirMenu(item)}>
              <Ionicons
                name="ellipsis-vertical"
                size={18}
                color="#666666fd"
                style={{ marginLeft: 5 }}
              />
            </TouchableOpacity>
          )}
        </View>
      </View>
    );
  };

  return (
    <KeyboardAvoidingView style={styles.container} behavior={Platform.OS === "ios" ? "padding" : "height"}>
      <Header navigation={null} nomeTela={topico} />


      <FlatList

        ref={flatListRef}
        data={mensagens}
        keyExtractor={(item) => item.id}
        renderItem={({ item, index }) => {
          const anterior = mensagens[index - 1];

          const mostrarData =
            !anterior ||
            formatarData(anterior.hora) !==
              formatarData(item.hora);

          return (
            <>
              {/* 📅 DATA */}
              {mostrarData && (
                <View style={styles.dataContainer}>
                  <Text style={styles.dataTexto}>
                    {formatarData(item.hora)}
                  </Text>
                </View>
              )}

              {/* 💬 MENSAGEM */}
              {renderItem({ item })}
            </>
          );
        }}
        contentContainerStyle={{
          padding: 15,
          paddingBottom: 120,
        }}
      />

      {/* ✍️ INPUT */}
      <View style={styles.inputContainer}>
        {/* ❌ CANCELAR EDIÇÃO */}
        {editandoId && (
          <TouchableOpacity
            onPress={() => {
              setEditandoId(null);
              setNovaMensagem("");
            }}
          >
            <Text style={{ color: "red", marginRight: 10 }}>
              Cancelar
            </Text>
          </TouchableOpacity>
        )}

        <TextInput
          value={novaMensagem}
          onChangeText={setNovaMensagem}
          placeholder={
            editandoId
              ? "Editando mensagem..."
              : "Digite sua mensagem..."
          }
          style={styles.input}
        />

        <TouchableOpacity style={styles.botao} onPress={enviarMensagem}>
          <Ionicons
            name={editandoId ? "checkmark" : "send"}
            size={20}
            color="#fff"
          />
        </TouchableOpacity>
      </View>

      
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#eaeef3", //eaeef3
    
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

  hora: {
    fontSize: 10,
    color: "#888",
    marginTop: 5,
    textAlign: "right",
  },

  dataContainer: {
    alignItems: "center",
    marginVertical: 10,
  },

  dataTexto: {
    backgroundColor: "#dfe6ee",
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 10,
    fontSize: 12,
    color: "#555",
  },

  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    padding: 10,
    backgroundColor: "#fff",
    borderTopWidth: 1,
    borderColor: "#ddd",
    bottom: 50,
  },

  input: {
    flex: 1,
    backgroundColor: "#ddd",
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