import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;


public class detectorSaltos {
	public static BufferedReader leerEntrada(String entrada) throws FileNotFoundException{
		BufferedReader res = new BufferedReader(new FileReader(entrada));
		return res;
	}
	
	public static void inicializarR(Double[] valoresR){
		double valor = 1.511;
		valoresR[3] = valor;
		valor = 1.4250;
		valoresR[4] = valor;
		valor = 1.5712;
		valoresR[5] = valor;
		valor = 1.6563;
		valoresR[6] = valor;
		valor = 1.7110;
		valoresR[7] = valor;
		valor = 1.7491;
		valoresR[8] = valor;
		valor = 1.7770;
		valoresR[9] = valor;
		valor = 1.7984;
		valoresR[10] = valor;
		valor = 1.8153;
		valoresR[11] = valor;
		valor = 1.8290;
		valoresR[12] = valor;
		valor = 1.8403;
		valoresR[13] = valor;
		valor = 1.8403;
		valoresR[14] = valor;
		valor = 1.8579;
		valoresR[15] = valor;
		valor = 1.8649;
		valoresR[16] = valor;
		valor = 1.8710;
		valoresR[17] = valor;
		valor = 1.8764;
		valoresR[18] = valor;
		valor = 1.8811;
		valoresR[19] = valor;
		valor = 1.8853;
		valoresR[20] = valor;
		valor = 1.8891;
		valoresR[21] = valor;
		valor = 1.8926;
		valoresR[22] = valor;
		valor = 1.8957;
		valoresR[23] = valor;
		valor = 1.8985;
		valoresR[24] = valor;
		valor = 1.9011;
		valoresR[25] = valor;
		valor = 1.9035;
		valoresR[26] = valor;
		valor = 1.9057;
		valoresR[27] = valor;
		valor = 1.9078;
		valoresR[28] = valor;
		valor = 1.9096;
		valoresR[29] = valor;
		valor = 1.9114;
		valoresR[30] = valor;
		valor = 1.9130;
		valoresR[31] = valor;
		valor = 1.9146;
		valoresR[32] = valor;
		valor = 1.9160;
		valoresR[33] = valor;
		valor = 1.9176;
		valoresR[34] = valor;
		valor = 1.9186;
		valoresR[35] = valor;
		valor = 1.9198;
		valoresR[36] = valor;
		valor = 1.9209;
		valoresR[37] = valor;
		valor = 1.9220;
		valoresR[38] = valor;
	}
	
	public static void main(String [] entradas) throws IOException{
		Double [] valoresR = new Double[39];
		inicializarR(valoresR);
		
		LinkedList<Double> diferencias = new LinkedList<Double>();
		LinkedList<String> ipDiferencias = new LinkedList<String>();
		LinkedList<String> ipEntrada = new LinkedList<String>();
		LinkedList<Double> datosEntrada = new LinkedList<Double>();
		HashMap<String,String> localizacion = new HashMap<String,String>();
		HashMap<String,Character> salto = new HashMap<String,Character>();
		if(entradas.length==0){
			System.out.print("<archivo_de_entrada>");
			return;
		}
		BufferedReader archivoEntrada = leerEntrada(entradas[0]);
		String dato = archivoEntrada.readLine();
		if(!dato.startsWith("Route")){
			System.out.print("error, archivo invalido");
		}
		while(!dato.equals("done!")){
			dato = archivoEntrada.readLine();
			String mediciones [] = dato.split("	");
			if(mediciones.length==1){
				ipEntrada.add("noResponde");
			}else{
				ipEntrada.add(mediciones[0]);
				datosEntrada.add(Double.parseDouble(mediciones[1])*1000);
				if(mediciones.length==3){
					localizacion.put(mediciones[0], mediciones[2]);
				}else{
					localizacion.put(mediciones[0], "None");
				}
			}
		}
		Iterator<String> it = ipEntrada.iterator();
		Iterator<Double> itDatos = datosEntrada.iterator();
		String anterior = "noResponde";
		double valorAnterior = 0;
		while(it.hasNext()){
			String actual = it.next();
			if(anterior.equals("noResponde") || actual.equals("noResponde")){
				anterior = actual;
			}else{
				double valorActual = itDatos.next();
				diferencias.add(valorActual-valorAnterior);
				ipDiferencias.add(anterior + "_" + actual);
				
				String localizacionAnterior = localizacion.get(anterior);
				String localizacionActual = localizacion.get(actual);
				if(localizacionAnterior.equals("None") || localizacionActual.equals("None")){
					salto.put(anterior + "_" + actual, 'u');
				}else{
					
					
					
					String anterior_continente = localizacionAnterior.split("/")[0];
					String actual_continente = localizacionActual.split("/")[0];
					if(anterior_continente.equals(actual_continente)){
						salto.put(anterior + "_" + actual, 'l');
					}else{
						salto.put(anterior + "_" + actual, 's');
					}
					
					//--------------------------------------------------------
					
					if(anterior.equals("64.124.200.234")){
						System.err.print(anterior_continente + "\n" + actual_continente+"\n");
					}
					
					//--------------------------------------------------------
					
				}
				
				anterior = actual;
				valorAnterior = valorActual;
			}
		}
		
		double esperanza = calcularEsperanza(diferencias);
		double varianza = calcularVarianza(diferencias,esperanza);
		Iterator<Double> itDif = diferencias.iterator();
		Iterator<String> itIpDif = ipDiferencias.iterator();
		while(itDif.hasNext()){
			double valor = itDif.next();
			String ip = itIpDif.next();
			int tamanio = diferencias.size();
			if(salto.get(ip).equals('u')){
				if(esOutlet(valor,esperanza,varianza,tamanio)){
					System.out.print(ip +  " salto_detectado desconocido\n");
				}else{
					System.out.print(ip +  " no_salto desconocido\n");
				}
			}else if(salto.get(ip).equals('s')){
				if(esOutlet(valor,esperanza,varianza,tamanio)){
					System.out.print(ip +  " salto_detectado correcto\n");
				}else{
					System.out.print(ip +  " no_salto FALLA\n");
				}
			}else{
				if(esOutlet(valor,esperanza,varianza,tamanio)){
					System.out.print(ip +  " salto_detectado FALLA\n");
				}else{
					System.out.print(ip +  " no_salto correcto\n");
				}
			}
			
		}
	}
	
	private static double calcularEsperanza(LinkedList<Double> entrada){
		int tamanio = entrada.size();
		Iterator<Double> it = entrada.iterator();
		int res = 0;
		while(it.hasNext()){
			res += (it.next())/tamanio;
		}
		return res;
	}
	
	private static double calcularVarianza(LinkedList<Double> entrada,double esperanza){
		int tamanio = entrada.size();
		int res = 0;
		Iterator<Double> it = entrada.iterator();
		while(it.hasNext()){
			double valor = it.next()-esperanza;
			res += valor*valor/tamanio;
		}
		return res;
	}
	
	private static boolean esOutlet(double dato,double esperanza, double r,int tamanio){
		return (r*esperanza) < (dato-esperanza);
	}
	
}
