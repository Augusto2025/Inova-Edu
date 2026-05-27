import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Switch,
  TouchableOpacity,
  Image,
} from "react-native";

import { Ionicons } from "@expo/vector-icons";

import Header from "../components/Header";
import ProfileScreen from "./Perfil";
import { COLORS } from "../components/Cores"; // Importando as cores para manter a consistência visual

export default function ConfiguracoesScreen({ navigation }) {

  const [som, setSom] = useState(false);
  const [vibracao, setVibracao] = useState(false);

  const [push, setPush] = useState(false);
  const [email, setEmail] = useState(false);
  const [mensagens, setMensagens] = useState(false);
  const [eventos, setEventos] = useState(false);

  const [duasEtapas, setDuasEtapas] = useState(false);

  const [modoEscuro, setModoEscuro] = useState(false);

  const irParaPerfil = () => {
    navigation.navigate("Perfil");
  }

  const ItemSwitch = ({
    icon,
    titulo,
    valor,
    funcao,
  }) => (

    <View style={styles.item}>

      <View style={styles.left}>

        <Ionicons
          name={icon}
          size={22}
          color="#444"
        />

        <Text style={styles.itemText}>
          {titulo}
        </Text>

      </View>

      <Switch
        value={valor}
        onValueChange={funcao}
      />

    </View>
  );

  const ItemBotao = ({
    icon,
    titulo,
    onPress,
  }) => (

    <TouchableOpacity
      style={styles.item}
      onPress={onPress}
    >

      <View style={styles.left}>

        <Ionicons
          name={icon}
          size={22}
          color="#444"
        />

        <Text style={styles.itemText}>
          {titulo}
        </Text>

      </View>

      <Ionicons
        name="chevron-forward"
        size={20}
        color="#777"
      />

    </TouchableOpacity>
  );

  return (

    <View style={styles.container}>

      <Header
        nomeTela={"Configurações"}
      />

      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{ paddingBottom: 120 }}
      >

        <View style={styles.perfil}>

          <Image
            source={require("../../assets/pascal.jpg")}
            style={styles.avatar}
          />

          <Text style={styles.nome}>
            Piaba Frita
          </Text>

          <Text style={styles.email}>
            piabafrita@email.com
          </Text>

          <TouchableOpacity style={styles.perfilBtn} onPress={irParaPerfil}>
            <Text style={styles.perfilBtnText}>
              Visualizar Perfil
            </Text>
          </TouchableOpacity>

        </View>

        {/* Repositório */}

        <Text style={styles.titulo}>
          Repositório
        </Text>

        <View style={styles.card}>

          <ItemBotao
            icon="download"
            titulo="Downloads automáticos"
          />

          <ItemBotao
            icon="cloud-upload"
            titulo="Backup automático"
          />

          <ItemBotao
            icon="folder"
            titulo="Arquivos recentes"
          />

        </View>

        {/* Notificações */}

        <Text style={styles.titulo}>
          Notificações
        </Text>

        <View style={styles.card}>

          <ItemSwitch
            icon="notifications"
            titulo="Notificações Push"
            valor={push}
            funcao={setPush}
          />

          <ItemSwitch
            icon="mail"
            titulo="Email"
            valor={email}
            funcao={setEmail}
          />

          <ItemSwitch
            icon="chatbox"
            titulo="Mensagens"
            valor={mensagens}
            funcao={setMensagens}
          />

          <ItemSwitch
            icon="calendar"
            titulo="Eventos"
            valor={eventos}
            funcao={setEventos}
          />

        </View>

        {/* Aparência */}

        <Text style={styles.titulo}>
          Aparência e Acessibilidade
        </Text>

        <View style={styles.card}>

          <ItemSwitch
            icon="moon"
            titulo="Modo Escuro"
            valor={modoEscuro}
            funcao={setModoEscuro}
          />

          <ItemBotao
            icon="text"
            titulo="Tamanho da fonte"
          />

          <ItemBotao
            icon="volume-high"
            titulo="Texto em voz alta"
          />

        </View>

        {/* Versão */}

        <Text style={styles.titulo}>
          Versão
        </Text>

        <View style={styles.card}>
          <Text style={{ color: "#777" }}>
            Versão Brasileira: Herbert Richers 1.0.0
          </Text>

        </View>

        <TouchableOpacity
          style={styles.logout}
        >

          <Ionicons
            name="log-out"
            size={24}
            color="#fff"
          />

          <Text style={styles.logoutText}>
            Sair do app
          </Text>

        </TouchableOpacity>

      </ScrollView>

    </View>

  );
}

const styles = StyleSheet.create({

  container: {
    flex: 1,
  },

  perfil: {
    alignItems: "center",
    marginBottom: 20,
  },

  avatar: {
    width: 120,
    height: 120,
    borderRadius: 60,
    borderWidth: 3,
    borderColor: "#2d6cdf"
  },

  nome: {
    fontSize: 24,
    fontWeight: "bold",
    color: COLORS.primary,
    marginTop: 10
  },

  email: {
    color: COLORS.darkBlue,
  },
  
  perfilBtn: {
    backgroundColor: COLORS.primary,
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 12,
    marginTop: 15,
  },

  perfilBtnText: {
    color: COLORS.background,
    fontWeight: 'bold',
  },

  titulo: {
    fontSize: 20,
    fontWeight: "bold",
    marginLeft: 15,
    marginBottom: 10,
    color: COLORS.primary
  },

  card: {
    backgroundColor: "#fff",
    marginHorizontal: 15,
    marginBottom: 20,
    borderRadius: 20,
    padding: 15,
    elevation: 4
  },

  item: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 15,
    borderBottomWidth: 1,
    borderBottomColor: "#EEE"
  },

  left: {
    flexDirection: "row",
    alignItems: "center"
  },

  itemText: {
    fontSize: 16,
    marginLeft: 10,
    color: "#333"
  },

  logout: {
    margin: 20,
    padding: 15,
    backgroundColor: "#ff5757",
    borderRadius: 15,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center"
  },

  logoutText: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "bold",
    marginLeft: 10
  }

});