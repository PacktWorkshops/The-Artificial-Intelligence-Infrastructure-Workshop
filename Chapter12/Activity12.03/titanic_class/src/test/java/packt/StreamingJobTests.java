package packt;

import org.jpmml.evaluator.Evaluator;
import org.jpmml.evaluator.InputField;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class StreamingJobTests {

    @Test
    public void canDeserializePmmlModel() {
        // arrange
        String fileName = "titanic_class.pmml";

        // act
        Evaluator evaluator = StreamingJob.getPmmlEvaluator(fileName);

        // assert
        assertEquals(evaluator.getMiningFunction().toString(), "classification");
    }

    @Test
    public void canGetFieldMap() {
        // arrange
        String fileName = "titanic_class.pmml";
        Evaluator evaluator = StreamingJob.getPmmlEvaluator(fileName);

        // act
        List<? extends InputField> inputFields = evaluator.getInputFields();

        // assert
        assertEquals(inputFields.size(), 6);
    }
}
