package gradescope;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.io.*;

class TestUtil {

    public static String readFile(String path) throws Exception {
        File file = new File(path);
        Scanner sc = new Scanner(file);
        String res = "";

        while (sc.hasNextLine()) {
            res += sc.nextLine() + "\n";
        }

        sc.close();

        return res.strip();
    }

    public static interface MainClass {
        void main(String[] args);
    }

    public static String runProgram(String inputPath, MainClass main) throws Exception {
        // Save IO streams
        InputStream input = System.in;
        PrintStream output = System.out;

        // Set the new IO streams
        System.setIn(new FileInputStream(inputPath));
        ByteArrayOutputStream myOut = new ByteArrayOutputStream();
        System.setOut(new PrintStream(myOut));

        // Run the program
        String[] args = null;
        main.main(args);

        // Reset the streams
        System.setIn(input);
        System.setOut(output);

        return myOut.toString().strip();
    }
}
