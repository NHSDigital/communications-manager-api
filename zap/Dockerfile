FROM zaproxy/zap-stable:2.17.0

COPY ./zap/policies/ /home/zap/.ZAP/policies/

RUN ./zap.sh -addoninstallall -cmd \
  && ./zap.sh -addonuninstall communityScripts -cmd \
  && ./zap.sh -addonuninstall packpentester -cmd \
  && ./zap.sh -addonuninstall wappalyzer -cmd
