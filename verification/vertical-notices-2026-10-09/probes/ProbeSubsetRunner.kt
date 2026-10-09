import org.junit.runner.JUnitCore
import org.junit.runner.Request
import org.junit.runner.Description
import org.junit.runner.manipulation.Filter
object ProbeSubsetRunner {
 @JvmStatic fun main(args: Array<String>) {
  val selected=args.drop(1).toSet()
  val request=Request.aClass(Class.forName(args[0])).filterWith(object: Filter() {
   override fun shouldRun(description: Description): Boolean = if(description.isTest) description.methodName.substringBefore("[") in selected else description.children.any {shouldRun(it)}
   override fun describe()="Exact selected methods: "+selected.joinToString(",")
  })
  val result=JUnitCore().run(request)
  println("RUN="+result.runCount+" FAIL="+result.failureCount+" IGNORED="+result.ignoreCount)
  result.failures.forEach {println(it.description.toString());println(it.trace)}
  kotlin.system.exitProcess(if(result.runCount==selected.size && result.failureCount==0 && result.ignoreCount==0) 0 else 1)
 }
}
