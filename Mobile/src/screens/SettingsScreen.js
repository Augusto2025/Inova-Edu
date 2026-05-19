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

export default function ConfiguracoesScreen({ navigation }) {

  const [som, setSom] = useState(true);
  const [vibracao, setVibracao] = useState(true);

  const [push, setPush] = useState(true);
  const [email, setEmail] = useState(true);
  const [mensagens, setMensagens] = useState(true);
  const [eventos, setEventos] = useState(false);

  const [duasEtapas, setDuasEtapas] = useState(false);

  const [modoEscuro, setModoEscuro] = useState(false);

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
        foto={null}
        escolherImagem={null}
        nomeTela={"Configurações"}
      />

      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={{ paddingBottom: 120 }}
      >

        <View style={styles.perfil}>

          {/* <Image
            source={require("../../assets/verdeerosa.jpg")}
            style={styles.avatar}
          /> */}

          <Text style={styles.nome}>
            Piaba Frita
          </Text>

          <Text style={styles.email}>
            piabafrita@email.com
          </Text>

        </View>

        {/* Geral */}

        <Text style={styles.titulo}>
          Geral
        </Text>

        <View style={styles.card}>

          <ItemSwitch
            icon="volume-high"
            titulo="Som do aplicativo"
            valor={som}
            funcao={setSom}
          />

          <ItemSwitch
            icon="phone-portrait"
            titulo="Vibração"
            valor={vibracao}
            funcao={setVibracao}
          />

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

        {/* Segurança */}

        <Text style={styles.titulo}>
          Segurança
        </Text>

        <View style={styles.card}>

          <ItemSwitch
            icon="shield-checkmark"
            titulo="Verificação em 2 etapas"
            valor={duasEtapas}
            funcao={setDuasEtapas}
          />

          <ItemBotao
            icon="lock-closed"
            titulo="Alterar senha"
          />

        </View>

        {/* Aparência */}

        <Text style={styles.titulo}>
          Aparência
        </Text>

        <View style={styles.card}>

          <ItemSwitch
            icon="moon"
            titulo="Modo Escuro"
            valor={modoEscuro}
            funcao={setModoEscuro}
          />

          <ItemBotao
            icon="color-palette"
            titulo="Tema"
          />

          <ItemBotao
            icon="text"
            titulo="Tamanho da fonte"
          />

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
            Sair da conta
          </Text>

        </TouchableOpacity>

      </ScrollView>

    </View>

  );
}

const styles = StyleSheet.create({

  container: {
    flex: 1,
    backgroundColor: "#F5F7FA",
  },

  perfil: {
    alignItems: "center",
    marginBottom: 30,
    marginTop: 20,
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
    color: "#333",
    marginTop: 10
  },

  email: {
    color: "#666"
  },

  titulo: {
    fontSize: 20,
    fontWeight: "bold",
    marginLeft: 15,
    marginBottom: 10,
    color: "#2d6cdf"
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