import React from "react";
import { Modal, View, Text, TextInput, TouchableOpacity, StyleSheet, TouchableWithoutFeedback } from "react-native";
import { COLORS } from "./Cores";

export default function ModalSave({ 
  modalEditarVisible,            
  setModalEditarVisible,         
  tituloModal = "Editar",        
  adicionarMaisInputs = false,   
  labelsInputs = [],             // 1. MUDANÇA AQUI: Recebe uma array com os nomes das labels, ex: ["Nome", "Telefone"]
  inputsExtras = [],             
  setInputsExtras,               
  salvarEdicao                   
}) {

  const handleInputChange = (text, index) => {
    const novosInputs = [...inputsExtras];
    novosInputs[index] = text;
    setInputsExtras(novosInputs);
  };

  return (
    <Modal visible={modalEditarVisible} animationType="slide" transparent={true}>
      <TouchableOpacity style={styles.modalOverlay} activeOpacity={1} onPress={() => setModalEditarVisible(false)}>
        
        <TouchableWithoutFeedback>
          <View style={styles.modalContent}>
            
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>{tituloModal}</Text>
            </View>

            <View style={styles.modalBody}>
              
              {/* 2. MUDANÇA AQUI: Agora fazemos o map diretamente na array de nomes recebida */}
              {adicionarMaisInputs && 
                labelsInputs.map((label, index) => (
                  <View key={index} style={styles.inputContainer}>
                    
                    {/* Exibe o nome exato que você enviou na lista */}
                    <Text style={styles.inputLabel}>{label}</Text>

                    <TextInput
                      style={styles.input}
                      placeholder={`Digite o ${label.toLowerCase()}`}
                      value={inputsExtras[index] || ""}
                      onChangeText={(text) => handleInputChange(text, index)}
                    />
                  </View>
                ))
              }

              <TouchableOpacity style={styles.saveBtn} onPress={salvarEdicao}>
                <Text style={styles.saveBtnText}>Salvar Alterações</Text>
              </TouchableOpacity>
            </View>

          </View>
        </TouchableWithoutFeedback>
        
      </TouchableOpacity>
    </Modal>
  );
}

const styles = StyleSheet.create({
  modalOverlay: { 
    flex: 1, 
    backgroundColor: 'rgba(0, 0, 0, 0.67)', 
    justifyContent: 'center', 
    padding: 15 
  },
  modalContent: { 
    backgroundColor: 'white', 
    borderRadius: 25, 
    overflow: 'hidden' 
  },
  modalHeader: { 
    backgroundColor: COLORS.primary, 
    flexDirection: 'row', 
    padding: 20, 
    alignItems: 'center',
    justifyContent: 'center' 
  },
  modalTitle: { 
    color: 'white', 
    fontSize: 18, 
    fontWeight: 'bold'
  },
  modalBody: { 
    padding: 20 
  },
  inputContainer: {
    marginBottom: 15 
  },
  inputLabel: {
    fontSize: 14,
    fontWeight: "600",
    color: "#333",
    marginBottom: 6, 
    paddingLeft: 2
  },
  input: { 
    borderWidth: 1, 
    borderColor: '#ddd', 
    borderRadius: 12, 
    padding: 12,
  },
  saveBtn: { 
    backgroundColor: COLORS.primary, 
    padding: 15, 
    borderRadius: 12, 
    alignItems: 'center',
    marginTop: 10 
  },
  saveBtnText: { 
    color: 'white', 
    fontWeight: 'bold' 
  }
});