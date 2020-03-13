/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package packt;

import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.serialization.SimpleStringEncoder;
import org.apache.flink.core.fs.Path;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.sink.filesystem.StreamingFileSink;
import org.dmg.pmml.FieldName;
import org.jpmml.evaluator.*;
import org.jpmml.evaluator.visitors.DefaultVisitorBattery;
import java.io.File;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;


/**
 * Skeleton for a Flink Streaming Job.
 *
 * <p>For a tutorial how to write a Flink streaming application, check the
 * tutorials and examples on the <a href="https://flink.apache.org/docs/stable/">Flink Website</a>.
 *
 * <p>To package your application into a JAR file for execution, run
 * 'mvn clean package' on the command line.
 *
 * <p>If you change the name of the main class (with the public static void main(String[] args))
 * method, change the respective entry in the POM.xml file (simply search for 'mainClass').
 */
public class StreamingJob {

	public static void main(String[] args) throws Exception {
		// prepare PMML evaluation
		ClassLoader classLoader = StreamingJob.class.getClassLoader();

		Evaluator evaluator = new LoadingModelEvaluatorBuilder()
				.setLocatable(false)
				.setVisitors(new DefaultVisitorBattery())
				.load(new File(classLoader.getResource("titanic.pmml").getFile()))
				.build();

		List<? extends InputField> inputFields = evaluator.getInputFields();

		// set up the streaming execution environment
		final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

		DataStream<String> dataStream = env.socketTextStream("localhost", 1234, "\n");

		SingleOutputStreamOperator<String> mapped = dataStream.map(new MapFunction<String, String>() {
			@Override
			public String map(String s) throws Exception {
				System.out.println("EVENT: " + s);

				Map<FieldName, FieldValue> arguments = getFieldMap(s, inputFields);

				// execute the model
				Map<FieldName, ?> results = evaluator.evaluate(arguments);

				// Decoupling results from the JPMML-Evaluator runtime environment
				Map<String, ?> resultRecord = EvaluatorUtil.decodeAll(results);

				System.out.println(resultRecord);
				return s;
			}
		});

		StreamingFileSink<String> sink = StreamingFileSink
				.forRowFormat(new Path("out"), new SimpleStringEncoder<String>("UTF-8"))
				.build();

		dataStream.addSink(sink);

		// execute program
		env.execute("Flink Streaming Java Titanic");
	}

	public static Map<FieldName, FieldValue> getFieldMap(String s, List<? extends InputField> inputFields) {
		Map<FieldName, FieldValue> arguments = new LinkedHashMap<>();
		String[] values = s.split(",");

		// prepare model evaluation
		for (int i = 0; i < values.length; i++) {
			FieldName inputName = inputFields.get(i).getName();
			FieldValue inputValue = inputFields.get(i).prepare(values[i]);
			arguments.put(inputName, inputValue);
		}

		return arguments;
	}
}
