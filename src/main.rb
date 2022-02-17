# Writes message into the output with yellow text color and 'Warning: ' prefix
def log_warn(message)
  warn "\e[33mWarning: #{message}\e[0m"
end

# Exits the program and writes message into the output with red color and
# 'Fatal: ' prefix
def log_abort(message)
  warn "\e[31mFatal: #{message}\e[0m"
  exit 1
end

begin
  require 'selenium-webdriver'
  require 'yaml'
  require 'json'
rescue LoadError => error
  log_abort "Failed to import required dependencies, ensure you have ran" \
            " `bundle` before executing the program (#{error})"
end

# Opens JSON file that contains tracked questions and converts it to array
# Returns an empty array if the file was not found or had syntax error
def open_tracked(path)
  path += '.json'

  begin
    file = File.open path, 'r'
    json = JSON.parse(file.read)
  rescue Exception => error
    log_warn "Unable to process '#{path}' file (#{error})"

    return []
  end

  json
end
