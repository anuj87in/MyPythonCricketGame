#!/bin/bash
################################################################################
# Kubernetes Inspector Script - Enhanced Edition
# Author: Anuj P| J S R! 🚩
#
# Features:
#   - ConfigMaps, Services, Secrets viewing
#   - Detailed Deployment inspection with auto-refresh
#   - StatefulSets, DaemonSets, Ingresses, PVCs
#   - Resource Usage Dashboard (CPU/Memory monitoring)
#   - Pod Logs Viewer (tail, follow, previous logs)
#   - Events Viewer (all, warnings only, by namespace)
#   - Pod Shell Access (bash/sh/custom commands)
#   - Interactive menus with countdown timers
#   - Clean UI with pause-and-continue flow
#
# Requirements:
#   - kubectl configured and connected to cluster
#   - jq (for JSON parsing)
#   - metrics-server (optional, for resource usage)
#
################################################################################

# Clear screen on first run
clear

# Function to pause and wait for user
pause() {
  echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  read -p "Press Enter to return to main menu..."
  clear
}

while true; do
  echo -e "
╔════════════════════════════════════════════════════╗
║     🚀 Kubernetes Inspector - J S R! 🚩         ║
╚════════════════════════════════════════════════════╝

Select an option to view Kubernetes resources:

📦 BASIC RESOURCES:
  1) ConfigMaps
  2) Services
  3) Secrets
  4) Deployments (Detailed Inspection)

🔍 ADVANCED RESOURCES:
  5) StatefulSets
  6) DaemonSets
  7) Ingresses
  8) PersistentVolumeClaims (PVCs)

📊 MONITORING & LOGS:
  9) Resource Usage (CPU/Memory)
  10) Pod Logs Viewer
  11) Events Viewer
  12) Problematic Pods Troubleshooter
  
💻 ACTIONS:
  13) Pod Shell Access
  
🚪 EXIT:
  14) Exit
"
  read -p "Enter your choice [1-14]: " choice

  case $choice in
    1)
      echo -e "\n📦 CONFIGMAPS VIEWER"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      
      # Get total count
      kubectl get configmaps --all-namespaces -o custom-columns="NAMESPACE:.metadata.namespace,NAME:.metadata.name" --no-headers > /tmp/configmaps.txt
      total_cms=$(wc -l < /tmp/configmaps.txt)
      
      echo -e "\n📊 Total ConfigMaps: $total_cms"
      echo -e "\n🔍 Options:"
      echo "1) Search by name/namespace"
      echo "2) List by namespace"
      echo "3) Show all (paginated)"
      echo "4) Return to main menu"
      read -p "Choose [1-4]: " cm_list_choice
      
      case $cm_list_choice in
        1)
          read -p "Enter search term (name or namespace): " search_term
          echo -e "\n📋 Matching ConfigMaps:"
          grep -i "$search_term" /tmp/configmaps.txt | nl
          ;;
        2)
          read -p "Enter namespace: " cm_ns_filter
          echo -e "\n📋 ConfigMaps in namespace: $cm_ns_filter"
          grep "^$cm_ns_filter " /tmp/configmaps.txt | nl
          ;;
        3)
          echo -e "\n📋 All ConfigMaps (showing first 50, use search to find specific ones):"
          head -50 /tmp/configmaps.txt | nl
          if [ "$total_cms" -gt 50 ]; then
            echo "... and $((total_cms - 50)) more. Use search option to find specific ConfigMaps."
          fi
          ;;
        4)
          clear
          continue
          ;;
        *)
          echo "❌ Invalid choice."
          pause
          continue
          ;;
      esac
      
      read -p $'\nEnter the number of the ConfigMap to view (or 0 to return): ' cm_choice
      
      if [ "$cm_choice" -eq 0 ] 2>/dev/null; then
        clear
      elif [ "$cm_choice" -gt 0 ] 2>/dev/null; then
        selected_cm_line=$(sed -n "${cm_choice}p" /tmp/configmaps.txt)
        cm_namespace=$(echo "$selected_cm_line" | awk '{print $1}')
        cm_name=$(echo "$selected_cm_line" | awk '{print $2}')
        
        if [ -n "$cm_namespace" ] && [ -n "$cm_name" ]; then
          while true; do
            echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "📦 ConfigMap: $cm_name"
            echo "📂 Namespace: $cm_namespace"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "1) View Data (YAML format)"
            echo "2) View Data (JSON format)"
            echo "3) Describe ConfigMap"
            echo "4) View Keys Only"
            echo "5) Return to Main Menu"
            read -p "Choose [1-5]: " cm_view_choice
            
            case $cm_view_choice in
              1)
                echo -e "\n📄 ConfigMap Data (YAML):"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                kubectl get configmap "$cm_name" -n "$cm_namespace" -o yaml
                ;;
              2)
                echo -e "\n📄 ConfigMap Data (JSON):"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                kubectl get configmap "$cm_name" -n "$cm_namespace" -o json | jq '.'
                ;;
              3)
                echo -e "\n📄 ConfigMap Description:"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                kubectl describe configmap "$cm_name" -n "$cm_namespace"
                ;;
              4)
                echo -e "\n🔑 ConfigMap Keys:"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                kubectl get configmap "$cm_name" -n "$cm_namespace" -o json | jq -r '.data | keys[]'
                ;;
              5)
                echo -e "\n✅ Returning to main menu..."
                sleep 1
                clear
                break
                ;;
              *)
                echo "❌ Invalid choice. Please select [1-5]."
                ;;
            esac
            
            if [ "$cm_view_choice" != "5" ]; then
              echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
              read -p "Press Enter to continue..."
            fi
          done
        else
          echo "❌ Error: Could not extract ConfigMap details."
          pause
        fi
      else
        echo "❌ Invalid choice."
        pause
      fi
      ;;
    2)
      echo -e "\n🔌 SERVICES VIEWER"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      
      # Get total count
      kubectl get services --all-namespaces -o custom-columns="NAMESPACE:.metadata.namespace,NAME:.metadata.name,TYPE:.spec.type" --no-headers > /tmp/services.txt
      total_svcs=$(wc -l < /tmp/services.txt)
      
      echo -e "\n📊 Total Services: $total_svcs"
      echo -e "\n🔍 Options:"
      echo "1) Search by name/namespace"
      echo "2) List by namespace"
      echo "3) Show all (paginated)"
      echo "4) Return to main menu"
      read -p "Choose [1-4]: " svc_list_choice
      
      case $svc_list_choice in
        1)
          read -p "Enter search term (name or namespace): " search_term
          echo -e "\n📋 Matching Services:"
          grep -i "$search_term" /tmp/services.txt | nl
          ;;
        2)
          read -p "Enter namespace: " svc_ns_filter
          echo -e "\n📋 Services in namespace: $svc_ns_filter"
          grep "^$svc_ns_filter " /tmp/services.txt | nl
          ;;
        3)
          echo -e "\n📋 All Services (showing first 50):"
          head -50 /tmp/services.txt | nl
          if [ "$total_svcs" -gt 50 ]; then
            echo "... and $((total_svcs - 50)) more. Use search option to find specific Services."
          fi
          ;;
        4)
          clear
          continue
          ;;
        *)
          echo "❌ Invalid choice."
          pause
          continue
          ;;
      esac
      
      read -p $'\nEnter the number of the Service to view (or 0 to return): ' svc_choice
      
      if [ "$svc_choice" -eq 0 ] 2>/dev/null; then
        clear
      elif [ "$svc_choice" -gt 0 ] 2>/dev/null; then
        selected_svc_line=$(sed -n "${svc_choice}p" /tmp/services.txt)
        svc_namespace=$(echo "$selected_svc_line" | awk '{print $1}')
        svc_name=$(echo "$selected_svc_line" | awk '{print $2}')
        
        if [ -n "$svc_namespace" ] && [ -n "$svc_name" ]; then
          while true; do
            echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "🔌 Service: $svc_name"
            echo "📂 Namespace: $svc_namespace"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "1) View Details (YAML)"
            echo "2) View Details (JSON)"
            echo "3) Describe Service"
            echo "4) View Endpoints"
            echo "5) Return to Main Menu"
            read -p "Choose [1-5]: " svc_view_choice
            
            case $svc_view_choice in
              1)
                echo -e "\n📄 Service Details (YAML):"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                kubectl get service "$svc_name" -n "$svc_namespace" -o yaml
                ;;
              2)
                echo -e "\n📄 Service Details (JSON):"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                kubectl get service "$svc_name" -n "$svc_namespace" -o json | jq '.'
                ;;
              3)
                echo -e "\n📄 Service Description:"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                kubectl describe service "$svc_name" -n "$svc_namespace"
                ;;
              4)
                echo -e "\n🎯 Service Endpoints:"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                kubectl get endpoints "$svc_name" -n "$svc_namespace" -o wide
                ;;
              5)
                echo -e "\n✅ Returning to main menu..."
                sleep 1
                clear
                break
                ;;
              *)
                echo "❌ Invalid choice. Please select [1-5]."
                ;;
            esac
            
            if [ "$svc_view_choice" != "5" ]; then
              echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
              read -p "Press Enter to continue..."
            fi
          done
        else
          echo "❌ Error: Could not extract Service details."
          pause
        fi
      else
        echo "❌ Invalid choice."
        pause
      fi
      ;;
    3)
      echo -e "\n🔐 SECRETS VIEWER"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      
      # Get total count
      kubectl get secrets --all-namespaces -o custom-columns="NAMESPACE:.metadata.namespace,NAME:.metadata.name,TYPE:.type" --no-headers > /tmp/secrets.txt
      total_secrets=$(wc -l < /tmp/secrets.txt)
      
      echo -e "\n📊 Total Secrets: $total_secrets"
      echo -e "\n🔍 Options:"
      echo "1) Search by name/namespace"
      echo "2) List by namespace"
      echo "3) Show all (paginated)"
      echo "4) Return to main menu"
      read -p "Choose [1-4]: " secret_list_choice
      
      case $secret_list_choice in
        1)
          read -p "Enter search term (name or namespace): " search_term
          echo -e "\n📋 Matching Secrets:"
          grep -i "$search_term" /tmp/secrets.txt | nl
          ;;
        2)
          read -p "Enter namespace: " secret_ns_filter
          echo -e "\n📋 Secrets in namespace: $secret_ns_filter"
          grep "^$secret_ns_filter " /tmp/secrets.txt | nl
          ;;
        3)
          echo -e "\n📋 All Secrets (showing first 50):"
          head -50 /tmp/secrets.txt | nl
          if [ "$total_secrets" -gt 50 ]; then
            echo "... and $((total_secrets - 50)) more. Use search option to find specific Secrets."
          fi
          ;;
        4)
          clear
          continue
          ;;
        *)
          echo "❌ Invalid choice."
          pause
          continue
          ;;
      esac
      
      read -p $'\nEnter the number of the Secret to view (or 0 to return): ' secret_choice
      
      if [ "$secret_choice" -eq 0 ] 2>/dev/null; then
        clear
      elif [ "$secret_choice" -gt 0 ] 2>/dev/null; then
        selected_secret_line=$(sed -n "${secret_choice}p" /tmp/secrets.txt)
        secret_namespace=$(echo "$selected_secret_line" | awk '{print $1}')
        secret_name=$(echo "$selected_secret_line" | awk '{print $2}')
        
        if [ -n "$secret_namespace" ] && [ -n "$secret_name" ]; then
          while true; do
            echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "🔐 Secret: $secret_name"
            echo "📂 Namespace: $secret_namespace"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "1) View Keys Only"
            echo "2) Describe Secret (without values)"
            echo "3) View Secret (YAML - base64 encoded)"
            echo "4) View Secret (Decoded values) ⚠️"
            echo "5) Return to Main Menu"
            read -p "Choose [1-5]: " secret_view_choice
            
            case $secret_view_choice in
              1)
                echo -e "\n🔑 Secret Keys:"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                kubectl get secret "$secret_name" -n "$secret_namespace" -o json | jq -r '.data | keys[]'
                ;;
              2)
                echo -e "\n📄 Secret Description:"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                kubectl describe secret "$secret_name" -n "$secret_namespace"
                ;;
              3)
                echo -e "\n📄 Secret (base64 encoded):"
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                kubectl get secret "$secret_name" -n "$secret_namespace" -o yaml
                ;;
              4)
                echo -e "\n⚠️  WARNING: This will display decoded secret values!"
                read -p "Are you sure? (yes/no): " confirm
                if [ "$confirm" == "yes" ]; then
                  echo -e "\n🔓 Secret Values (DECODED):"
                  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                  kubectl get secret "$secret_name" -n "$secret_namespace" -o json | jq -r '.data | to_entries[] | "\(.key): \(.value | @base64d)"'
                else
                  echo "❌ Cancelled."
                fi
                ;;
              5)
                echo -e "\n✅ Returning to main menu..."
                sleep 1
                clear
                break
                ;;
              *)
                echo "❌ Invalid choice. Please select [1-5]."
                ;;
            esac
            
            if [ "$secret_view_choice" != "5" ]; then
              echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
              read -p "Press Enter to continue..."
            fi
          done
        else
          echo "❌ Error: Could not extract Secret details."
          pause
        fi
      else
        echo "❌ Invalid choice."
        pause
      fi
      ;;
    4)
      echo -e "\n🚀 DEPLOYMENTS VIEWER"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      echo -e "\n📋 Select viewing mode:"
      echo "1) View All Deployments (All Namespaces)"
      echo "2) Filter by Namespace First"
      echo "3) Return to Main Menu"
      read -p "Choose [1-3]: " deploy_mode
      
      case $deploy_mode in
        1)
          # Mode 1: Show all deployments
          echo -e "\n🚀 Deployments in all namespaces:"
          kubectl get deployments --all-namespaces -o custom-columns="NAMESPACE:.metadata.namespace,DEPLOYMENT:.metadata.name" --no-headers > /tmp/deployments.txt
          total_deps=$(wc -l < /tmp/deployments.txt)
          echo -e "📊 Total Deployments: $total_deps\n"
          nl /tmp/deployments.txt
          
          read -p $'\nEnter the number of the deployment you want to inspect (or 0 to return): ' dep_choice
          
          if [ "$dep_choice" -eq 0 ] 2>/dev/null; then
            clear
            continue
          fi
          
          selected_line=$(sed -n "${dep_choice}p" /tmp/deployments.txt)
          namespace=$(echo $selected_line | awk '{print $1}')
          deployment=$(echo $selected_line | awk '{print $2}')
          ;;
        2)
          # Mode 2: Filter by namespace first
          echo -e "\n📂 Available Namespaces:"
          kubectl get namespaces -o custom-columns="NAMESPACE:.metadata.name,STATUS:.status.phase,AGE:.metadata.creationTimestamp" --no-headers > /tmp/namespaces_deploy.txt
          nl /tmp/namespaces_deploy.txt
          
          read -p $'\nEnter the number of the namespace (or 0 to return): ' ns_choice
          
          if [ "$ns_choice" -eq 0 ] 2>/dev/null; then
            clear
            continue
          fi
          
          selected_ns_line=$(sed -n "${ns_choice}p" /tmp/namespaces_deploy.txt)
          selected_namespace=$(echo $selected_ns_line | awk '{print $1}')
          
          if [ -z "$selected_namespace" ]; then
            echo "❌ Invalid namespace selection."
            pause
            continue
          fi
          
          echo -e "\n🚀 Deployments in namespace: $selected_namespace"
          kubectl get deployments -n "$selected_namespace" -o custom-columns="DEPLOYMENT:.metadata.name,REPLICAS:.spec.replicas,READY:.status.readyReplicas,AVAILABLE:.status.availableReplicas" --no-headers > /tmp/deployments_filtered.txt
          
          if [ ! -s /tmp/deployments_filtered.txt ]; then
            echo "⚠️  No deployments found in namespace: $selected_namespace"
            pause
            continue
          fi
          
          total_deps_ns=$(wc -l < /tmp/deployments_filtered.txt)
          echo -e "📊 Total Deployments in $selected_namespace: $total_deps_ns\n"
          nl /tmp/deployments_filtered.txt
          
          read -p $'\nEnter the number of the deployment you want to inspect (or 0 to return): ' dep_choice
          
          if [ "$dep_choice" -eq 0 ] 2>/dev/null; then
            clear
            continue
          fi
          
          selected_dep_line=$(sed -n "${dep_choice}p" /tmp/deployments_filtered.txt)
          deployment=$(echo $selected_dep_line | awk '{print $1}')
          namespace=$selected_namespace
          ;;
        3)
          clear
          continue
          ;;
        *)
          echo "❌ Invalid choice."
          pause
          continue
          ;;
      esac
      
      # Validate deployment selection
      if [ -z "$namespace" ] || [ -z "$deployment" ]; then
        echo "❌ Invalid deployment selection."
        pause
        continue
      fi

      echo -e "
🔍 Selected Deployment: $deployment"
      echo "📦 Namespace: $namespace"

      echo -e "
📋 ReplicaSets:"
      kubectl get rs -n "$namespace" --selector=app="$deployment"

      echo -e "
🐳 Pods:"
      kubectl get pods -n "$namespace" --selector=app="$deployment"

      echo -e "
🔍 Container Status in Pods:"
      pods=$(kubectl get pods -n "$namespace" -l app="$deployment" -o jsonpath="{.items[*].metadata.name}")
      for pod in $pods; do
        echo -e "
📦 Pod: $pod"
        kubectl get pod "$pod" -n "$namespace" -o json | jq -r '.status.containerStatuses[] | "\(.name): \(.state)"'
      done

while true; do
  echo -e "
Do you want to inspect another deployment? (y/N)"
  echo "⏳ If no input received in 15 seconds, then Inspector will refresh stats for previously selected deployment."
  echo -n "Your choice: "

  (
    for i in {15..1}; do
      echo -ne "\rWaiting: $i seconds...  "
      sleep 1
    done
    echo -ne "\r                          \r"
  ) &

  countdown_pid=$!
  read -t 15 answer
  read_status=$?
  kill $countdown_pid 2>/dev/null
  wait $countdown_pid 2>/dev/null
  echo -ne "\r                          \r"

  if [ $read_status -eq 0 ]; then
    if [ "$answer" == "y" ] || [ "$answer" == "Y" ]; then
      echo -e "\n📋 Select viewing mode:"
      echo "1) View All Deployments (All Namespaces)"
      echo "2) Filter by Namespace First"
      read -p "Choose [1-2]: " deploy_mode_refresh
      
      case $deploy_mode_refresh in
        1)
          # Mode 1: Show all deployments
          echo -e "\n🚀 Deployments in all namespaces:"
          kubectl get deployments --all-namespaces -o custom-columns="NAMESPACE:.metadata.namespace,DEPLOYMENT:.metadata.name" --no-headers > /tmp/deployments.txt
          total_deps=$(wc -l < /tmp/deployments.txt)
          echo -e "📊 Total Deployments: $total_deps\n"
          nl /tmp/deployments.txt
          read -p $'Enter the number of the deployment you want to inspect: ' dep_choice
          selected_line=$(sed -n "${dep_choice}p" /tmp/deployments.txt)
          namespace=$(echo $selected_line | awk '{print $1}')
          deployment=$(echo $selected_line | awk '{print $2}')
          ;;
        2)
          # Mode 2: Filter by namespace first
          echo -e "\n📂 Available Namespaces:"
          kubectl get namespaces -o custom-columns="NAMESPACE:.metadata.name,STATUS:.status.phase" --no-headers > /tmp/namespaces_deploy_refresh.txt
          nl /tmp/namespaces_deploy_refresh.txt
          read -p $'\nEnter the number of the namespace: ' ns_choice
          selected_ns_line=$(sed -n "${ns_choice}p" /tmp/namespaces_deploy_refresh.txt)
          selected_namespace=$(echo $selected_ns_line | awk '{print $1}')
          
          echo -e "\n🚀 Deployments in namespace: $selected_namespace"
          kubectl get deployments -n "$selected_namespace" -o custom-columns="DEPLOYMENT:.metadata.name,REPLICAS:.spec.replicas,READY:.status.readyReplicas" --no-headers > /tmp/deployments_filtered_refresh.txt
          total_deps_ns=$(wc -l < /tmp/deployments_filtered_refresh.txt)
          echo -e "📊 Total Deployments: $total_deps_ns\n"
          nl /tmp/deployments_filtered_refresh.txt
          read -p $'Enter the number of the deployment you want to inspect: ' dep_choice
          selected_dep_line=$(sed -n "${dep_choice}p" /tmp/deployments_filtered_refresh.txt)
          deployment=$(echo $selected_dep_line | awk '{print $1}')
          namespace=$selected_namespace
          ;;
        *)
          echo "❌ Invalid choice. Keeping current deployment."
          ;;
      esac
    else
      echo -e "\n✅ Returning to main menu..."
      sleep 1
      clear
      break
    fi
  fi

  echo -e "
⏳ No input received. Refreshing stats for previously selected deployment..."
  echo -e "
📋 ReplicaSets:"
  kubectl get rs -n "$namespace" --selector=app="$deployment"

  echo -e "
🐳 Pods:"
  kubectl get pods -n "$namespace" --selector=app="$deployment"

  echo -e "
🔍 Container Status in Pods:"
  pods=$(kubectl get pods -n "$namespace" -l app="$deployment" -o jsonpath='{.items[*].metadata.name}')
  for pod in $pods; do
    echo -e "
📦 Pod: $pod"
    kubectl get pod "$pod" -n "$namespace" -o json | jq -r '.status.containerStatuses[] | "\(.name): \(.state)"'
  done

done

      ;;
    5)
      echo -e "\n🔧 StatefulSets in all namespaces:"
      kubectl get statefulsets --all-namespaces
      pause
      ;;
    6)
      echo -e "\n⚙️  DaemonSets in all namespaces:"
      kubectl get daemonsets --all-namespaces
      pause
      ;;
    7)
      echo -e "\n🌐 Ingresses in all namespaces:"
      kubectl get ingresses --all-namespaces
      pause
      ;;
    8)
      echo -e "\n💾 PersistentVolumeClaims in all namespaces:"
      kubectl get pvc --all-namespaces
      pause
      ;;
    9)
      echo -e "\n📊 RESOURCE USAGE DASHBOARD"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      echo -e "\n🖥️  Node Resource Usage:"
      kubectl top nodes 2>/dev/null || echo "❌ Metrics server not available. Install with: kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml"
      
      echo -e "\n🐳 Top 20 Pods by CPU Usage (with % of requests/limits):"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      
      # Get pod metrics and resource requests/limits
      kubectl get pods --all-namespaces -o json 2>/dev/null | jq -r '
        .items[] | 
        {
          namespace: .metadata.namespace,
          name: .metadata.name,
          cpuRequest: ([.spec.containers[].resources.requests.cpu // "0"] | map(
            if test("m$") then (.[:-1] | tonumber)
            else (. | tonumber) * 1000
            end
          ) | add),
          cpuLimit: ([.spec.containers[].resources.limits.cpu // "0"] | map(
            if test("m$") then (.[:-1] | tonumber)
            else (. | tonumber) * 1000
            end
          ) | add),
          memRequest: ([.spec.containers[].resources.requests.memory // "0"] | map(
            if test("Mi$") then (.[:-2] | tonumber)
            elif test("Gi$") then (.[:-2] | tonumber) * 1024
            elif test("Ki$") then (.[:-2] | tonumber) / 1024
            else (. | tonumber) / 1048576
            end
          ) | add),
          memLimit: ([.spec.containers[].resources.limits.memory // "0"] | map(
            if test("Mi$") then (.[:-2] | tonumber)
            elif test("Gi$") then (.[:-2] | tonumber) * 1024
            elif test("Ki$") then (.[:-2] | tonumber) / 1024
            else (. | tonumber) / 1048576
            end
          ) | add)
        } |
        [.namespace, .name, (.cpuRequest | tostring), (.cpuLimit | tostring), (.memRequest | tostring), (.memLimit | tostring)] | @tsv
      ' > /tmp/pod_resources.txt 2>/dev/null
      
      kubectl top pods --all-namespaces 2>/dev/null | tail -n +2 > /tmp/pod_usage.txt
      
      if [ -s /tmp/pod_usage.txt ]; then
        printf "%-25s %-45s %-18s %-18s\n" "NAMESPACE" "POD" "CPU" "MEMORY"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        while read -r ns pod cpu mem; do
          # Convert CPU to millicores
          if [[ $cpu == *m ]]; then
            cpu_num=${cpu%m}
          else
            cpu_num=$((${cpu%m} * 1000))
          fi
          
          # Convert memory to Mi
          if [[ $mem == *Mi ]]; then
            mem_num=${mem%Mi}
          elif [[ $mem == *Gi ]]; then
            mem_num=$((${mem%Gi} * 1024))
          elif [[ $mem == *Ki ]]; then
            mem_num=$((${mem%Ki} / 1024))
          else
            mem_num=$mem
          fi
          
          # Get resource requests/limits
          resource_line=$(grep "^$ns"$'\t'"$pod"$'\t' /tmp/pod_resources.txt 2>/dev/null)
          if [ -n "$resource_line" ]; then
            cpu_req=$(echo "$resource_line" | cut -f3)
            cpu_lim=$(echo "$resource_line" | cut -f4)
            mem_req=$(echo "$resource_line" | cut -f5)
            mem_lim=$(echo "$resource_line" | cut -f6)
            
            # Calculate CPU percentage
            if [ "$cpu_req" != "0" ] && [ "$cpu_req" != "" ]; then
              cpu_pct=$(awk "BEGIN {printf \"%.0f\", ($cpu_num / $cpu_req) * 100}")
              cpu_display="${cpu} (${cpu_pct}%)"
            else
              cpu_display="${cpu} (N/A)"
            fi
            
            # Calculate Memory percentage
            if [ "$mem_req" != "0" ] && [ "$mem_req" != "" ]; then
              mem_pct=$(awk "BEGIN {printf \"%.0f\", ($mem_num / $mem_req) * 100}")
              mem_display="${mem} (${mem_pct}%)"
            else
              mem_display="${mem} (N/A)"
            fi
          else
            cpu_display="${cpu} (N/A)"
            mem_display="${mem} (N/A)"
          fi
          
          printf "%-25s %-45s %-18s %-18s\n" \
            "${ns:0:25}" "${pod:0:45}" "$cpu_display" "$mem_display"
        done < <(sort -t' ' -k3 -rh /tmp/pod_usage.txt | head -20)
      else
        echo "❌ Metrics server not available"
      fi
      
      echo -e "\n💾 Top 20 Pods by Memory Usage (with % of requests/limits):"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      
      if [ -s /tmp/pod_usage.txt ]; then
        printf "%-25s %-45s %-18s %-18s\n" "NAMESPACE" "POD" "CPU" "MEMORY"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        while read -r ns pod cpu mem; do
          # Convert CPU to millicores
          if [[ $cpu == *m ]]; then
            cpu_num=${cpu%m}
          else
            cpu_num=$((${cpu%m} * 1000))
          fi
          
          # Convert memory to Mi
          if [[ $mem == *Mi ]]; then
            mem_num=${mem%Mi}
          elif [[ $mem == *Gi ]]; then
            mem_num=$((${mem%Gi} * 1024))
          elif [[ $mem == *Ki ]]; then
            mem_num=$((${mem%Ki} / 1024))
          else
            mem_num=$mem
          fi
          
          # Get resource requests/limits
          resource_line=$(grep "^$ns"$'\t'"$pod"$'\t' /tmp/pod_resources.txt 2>/dev/null)
          if [ -n "$resource_line" ]; then
            cpu_req=$(echo "$resource_line" | cut -f3)
            cpu_lim=$(echo "$resource_line" | cut -f4)
            mem_req=$(echo "$resource_line" | cut -f5)
            mem_lim=$(echo "$resource_line" | cut -f6)
            
            # Calculate CPU percentage
            if [ "$cpu_req" != "0" ] && [ "$cpu_req" != "" ]; then
              cpu_pct=$(awk "BEGIN {printf \"%.0f\", ($cpu_num / $cpu_req) * 100}")
              cpu_display="${cpu} (${cpu_pct}%)"
            else
              cpu_display="${cpu} (N/A)"
            fi
            
            # Calculate Memory percentage
            if [ "$mem_req" != "0" ] && [ "$mem_req" != "" ]; then
              mem_pct=$(awk "BEGIN {printf \"%.0f\", ($mem_num / $mem_req) * 100}")
              mem_display="${mem} (${mem_pct}%)"
            else
              mem_display="${mem} (N/A)"
            fi
          else
            cpu_display="${cpu} (N/A)"
            mem_display="${mem} (N/A)"
          fi
          
          printf "%-25s %-45s %-18s %-18s\n" \
            "${ns:0:25}" "${pod:0:45}" "$cpu_display" "$mem_display"
        done < <(sort -t' ' -k4 -rh /tmp/pod_usage.txt | head -20)
      else
        echo "❌ Metrics server not available"
      fi
      
      pause
      ;;
    10)
      echo -e "\n📜 POD LOGS VIEWER"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      
      # List all pods
      echo -e "\n🐳 Available Pods:"
      kubectl get pods --all-namespaces -o custom-columns="NAMESPACE:.metadata.namespace,POD:.metadata.name,STATUS:.status.phase" --no-headers > /tmp/pods.txt
      nl /tmp/pods.txt
      
      read -p $'\nEnter the number of the pod to view logs: ' pod_choice
      selected_pod_line=$(sed -n "${pod_choice}p" /tmp/pods.txt)
      pod_namespace=$(echo $selected_pod_line | awk '{print $1}')
      pod_name=$(echo $selected_pod_line | awk '{print $2}')
      
      # Get containers in the pod
      containers=$(kubectl get pod "$pod_name" -n "$pod_namespace" -o jsonpath='{.spec.containers[*].name}')
      container_array=($containers)
      
      if [ ${#container_array[@]} -eq 1 ]; then
        selected_container=${container_array[0]}
        echo -e "\n📦 Single container found: $selected_container"
      else
        echo -e "\n📦 Multiple containers found. Select one:"
        select selected_container in "${container_array[@]}"; do
          if [ -n "$selected_container" ]; then
            break
          fi
        done
      fi
      
      echo -e "\n📜 Log Options:"
      echo "1) View last 50 lines"
      echo "2) View last 100 lines"
      echo "3) View last 500 lines"
      echo "4) Follow logs (real-time)"
      echo "5) View previous container logs (for crashed pods)"
      read -p "Choose an option [1-5]: " log_option
      
      case $log_option in
        1)
          kubectl logs "$pod_name" -n "$pod_namespace" -c "$selected_container" --tail=50
          ;;
        2)
          kubectl logs "$pod_name" -n "$pod_namespace" -c "$selected_container" --tail=100
          ;;
        3)
          kubectl logs "$pod_name" -n "$pod_namespace" -c "$selected_container" --tail=500
          ;;
        4)
          echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
          echo "📡 Following logs in real-time..."
          echo "⚠️  Press Ctrl+C to stop following logs and return to menu"
          echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
          echo ""
          # Run kubectl logs in a subshell with trap to catch Ctrl+C
          (
            trap 'echo -e "\n\n✅ Stopped following logs."; exit 0' INT
            kubectl logs "$pod_name" -n "$pod_namespace" -c "$selected_container" -f
          )
          # After Ctrl+C or natural exit, continue
          echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
          ;;
        5)
          kubectl logs "$pod_name" -n "$pod_namespace" -c "$selected_container" --previous
          ;;
        *)
          kubectl logs "$pod_name" -n "$pod_namespace" -c "$selected_container" --tail=50
          ;;
      esac
      pause
      ;;
    11)
      echo -e "\n🔔 EVENTS VIEWER"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      echo "1) All Events (All Namespaces)"
      echo "2) Warning Events Only"
      echo "3) Events for Specific Namespace"
      read -p "Choose an option [1-3]: " event_option
      
      case $event_option in
        1)
          echo -e "\n📋 All Events (sorted by timestamp):"
          kubectl get events --all-namespaces --sort-by='.lastTimestamp'
          ;;
        2)
          echo -e "\n⚠️  Warning Events:"
          kubectl get events --all-namespaces --field-selector type=Warning --sort-by='.lastTimestamp'
          ;;
        3)
          echo -e "\n📂 Available Namespaces:"
          kubectl get namespaces -o custom-columns="NAMESPACE:.metadata.name,STATUS:.status.phase,AGE:.metadata.creationTimestamp" --no-headers > /tmp/namespaces.txt
          nl /tmp/namespaces.txt
          
          read -p $'\nEnter the number of the namespace: ' ns_choice
          selected_ns_line=$(sed -n "${ns_choice}p" /tmp/namespaces.txt)
          event_namespace=$(echo $selected_ns_line | awk '{print $1}')
          
          echo -e "\n📋 Events in namespace: $event_namespace"
          kubectl get events -n "$event_namespace" --sort-by='.lastTimestamp'
          ;;
        *)
          kubectl get events --all-namespaces --sort-by='.lastTimestamp'
          ;;
      esac
      pause
      ;;
    12)
      echo -e "\n🚨 PROBLEMATIC PODS TROUBLESHOOTER"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      echo -e "\n📋 Detection Criteria:"
      echo "  • Pods not in Running/Succeeded state"
      echo "  • Pods in error states (CrashLoopBackOff, ImagePullBackOff, etc.)"
      echo "  • Pods restarted within last 10 minutes"
      echo -e "\n🔍 Scanning for problematic pods...\n"
      
      # Get current time
      current_epoch=$(date +%s)
      
      # Get all pods with status and restart count
      kubectl get pods --all-namespaces -o json | jq -r --arg current_time "$current_epoch" '
        def parse_k8s_time:
          if . == null then 0
          else (. | fromdateiso8601)
          end;
        
        def time_ago:
          if . == 0 then "Never"
          else 
            (($current_time | tonumber) - .) | 
            if . < 0 then "0"
            else tostring
            end
          end;
        
        [.items[] |
        {
          namespace: .metadata.namespace,
          name: .metadata.name,
          phase: .status.phase,
          maxRestarts: ([.status.containerStatuses[]?.restartCount // 0] | max),
          lastRestartTime: ([.status.containerStatuses[]?.lastState.terminated.finishedAt // null] | map(parse_k8s_time) | max // 0),
          reason: (
            if (.status.containerStatuses[]?.state.waiting.reason) then
              ([.status.containerStatuses[] | select(.state.waiting) | .state.waiting.reason] | first) // "N/A"
            elif (.status.containerStatuses[]?.state.terminated.reason) then
              ([.status.containerStatuses[] | select(.state.terminated) | .state.terminated.reason] | first) // "N/A"
            else
              .status.reason // "N/A"
            end
          ),
          timestamp: .metadata.creationTimestamp
        } |
        . + {secondsSinceRestart: (.lastRestartTime | time_ago)} |
        select(
          (.phase != "Running" and .phase != "Succeeded") or
          (.reason | test("CrashLoopBackOff|ImagePullBackOff|ErrImagePull|CreateContainerConfigError|InvalidImageName|OOMKilled|Error")) or
          ((.secondsSinceRestart != "Never") and ((.secondsSinceRestart | tonumber) <= 600))
        )] |
        unique_by(.namespace + .name) |
        .[] |
        [.namespace, .name, .phase, (.maxRestarts | tostring), .secondsSinceRestart, .reason, .timestamp] | @tsv
      ' | sort -k4,4nr -k5,5n > /tmp/problematic_pods.txt
      
      # Check if any problematic pods found
      if [ ! -s /tmp/problematic_pods.txt ]; then
        echo "✅ No problematic pods found! All pods are healthy."
        pause
      else
        echo -e "⚠️  Found problematic pods:\n"
        echo "┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓"
        printf "┃ %-3s ┃ %-20s ┃ %-38s ┃ %-14s ┃ %-21s ┃ %-20s ┃\n" "NUM" "NAMESPACE" "POD" "STATUS" "RESTARTS" "REASON"
        echo "┣━━━━━╋━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━┓"
        
        line_num=0
        while IFS=$'\t' read -r namespace pod status restarts seconds_ago reason timestamp; do
          line_num=$((line_num + 1))
          
          # Format the restart info with last restart time
          if [ "$seconds_ago" == "Never" ] || [ "$seconds_ago" == "0" ]; then
            restart_display="$restarts - (Stable)"
          else
            restart_display="$restarts - ($seconds_ago s ago)"
          fi
          
          printf "┃ %-3s ┃ %-20s ┃ %-38s ┃ %-14s ┃ %-21s ┃ %-20s ┃\n" \
            "$line_num" \
            "${namespace:0:20}" \
            "${pod:0:38}" \
            "${status:0:14}" \
            "${restart_display:0:21}" \
            "${reason:0:20}"
        done < /tmp/problematic_pods.txt
        
        echo "┗━━━━━┻━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━┛"
        
        read -p $'\nEnter the number of the pod to troubleshoot (or 0 to return): ' problem_pod_choice
        
        if [ "$problem_pod_choice" -eq 0 ] 2>/dev/null; then
          clear
        elif [ "$problem_pod_choice" -gt 0 ] 2>/dev/null && [ "$problem_pod_choice" -le "$line_num" ]; then
          selected_problem_line=$(sed -n "${problem_pod_choice}p" /tmp/problematic_pods.txt)
          problem_namespace=$(echo "$selected_problem_line" | cut -f1)
          problem_pod=$(echo "$selected_problem_line" | cut -f2)
          problem_status=$(echo "$selected_problem_line" | cut -f3)
          
          if [ -z "$problem_namespace" ] || [ -z "$problem_pod" ]; then
            echo -e "\n❌ Error: Could not extract pod details. Please try again."
            pause
          else
            echo -e "\n🔧 Troubleshooting Pod: $problem_pod"
            echo "📦 Namespace: $problem_namespace"
            echo "⚠️  Status: $problem_status"
            
            # Get containers in the problematic pod
            problem_containers=$(kubectl get pod "$problem_pod" -n "$problem_namespace" -o jsonpath='{.spec.containers[*].name}')
            problem_container_array=($problem_containers)
            container_count=${#problem_container_array[@]}
            
            echo -e "📦 Total Containers: $container_count"
            
            # Troubleshooting menu (pod level first)
            while true; do
              echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
              echo "🔍 Troubleshooting Options:"
              echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
              echo "1) View Pod Description & Events"
              echo "2) View All Container Status Details"
              echo "3) View Container Logs"
              echo "4) View Previous Container Logs (if crashed)"
              echo "5) Follow Container Logs (real-time)"
              echo "6) Return to Main Menu"
              read -p "Choose [1-6]: " troubleshoot_choice
              
              case $troubleshoot_choice in
                1)
                  echo -e "\n📋 Pod Description & Events:"
                  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                  kubectl describe pod "$problem_pod" -n "$problem_namespace"
                  ;;
                2)
                  echo -e "\n🔍 All Container Status Details:"
                  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                  kubectl get pod "$problem_pod" -n "$problem_namespace" -o json | jq -r '.status.containerStatuses[] | 
                    "Container: \(.name)\n" +
                    "Ready: \(.ready)\n" +
                    "Restart Count: \(.restartCount)\n" +
                    "State: \(.state | keys[0])\n" +
                    "State Details: \(.state | to_entries[0].value)\n" +
                    "Last State: \(.lastState | keys[0] // "N/A")\n" +
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"'
                  ;;
                3)
                  # Now select container for logs
                  echo -e "\n📦 Select container to view logs:"
                  if [ $container_count -eq 1 ]; then
                    selected_problem_container=${problem_container_array[0]}
                    echo "  → Only one container: $selected_problem_container"
                  else
                    for i in "${!problem_container_array[@]}"; do
                      echo "  $((i+1))) ${problem_container_array[$i]}"
                    done
                    read -p "Choose container [1-$container_count]: " container_choice
                    selected_problem_container=${problem_container_array[$((container_choice-1))]}
                  fi
                  
                  echo -e "\n📜 Current Logs from $selected_problem_container (last 100 lines):"
                  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                  kubectl logs "$problem_pod" -n "$problem_namespace" -c "$selected_problem_container" --tail=100 2>&1
                  ;;
                4)
                  # Select container for previous logs
                  echo -e "\n📦 Select container to view previous logs:"
                  if [ $container_count -eq 1 ]; then
                    selected_problem_container=${problem_container_array[0]}
                    echo "  → Only one container: $selected_problem_container"
                  else
                    for i in "${!problem_container_array[@]}"; do
                      echo "  $((i+1))) ${problem_container_array[$i]}"
                    done
                    read -p "Choose container [1-$container_count]: " container_choice
                    selected_problem_container=${problem_container_array[$((container_choice-1))]}
                  fi
                  
                  echo -e "\n📜 Previous Logs from $selected_problem_container:"
                  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                  kubectl logs "$problem_pod" -n "$problem_namespace" -c "$selected_problem_container" --previous 2>&1 || echo "❌ No previous logs available (container may not have restarted yet)"
                  ;;
                5)
                  # Select container to follow logs
                  echo -e "\n📦 Select container to follow logs:"
                  if [ $container_count -eq 1 ]; then
                    selected_problem_container=${problem_container_array[0]}
                    echo "  → Only one container: $selected_problem_container"
                  else
                    for i in "${!problem_container_array[@]}"; do
                      echo "  $((i+1))) ${problem_container_array[$i]}"
                    done
                    read -p "Choose container [1-$container_count]: " container_choice
                    selected_problem_container=${problem_container_array[$((container_choice-1))]}
                  fi
                  
                  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                  echo "📡 Following logs from $selected_problem_container in real-time..."
                  echo "⚠️  Press Ctrl+C to stop following logs"
                  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                  echo ""
                  (
                    trap 'echo -e "\n\n✅ Stopped following logs."; exit 0' INT
                    kubectl logs "$problem_pod" -n "$problem_namespace" -c "$selected_problem_container" -f 2>&1
                  )
                  echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                  ;;
                6)
                  echo -e "\n✅ Returning to main menu..."
                  sleep 1
                  clear
                  break
                  ;;
                *)
                  echo "❌ Invalid choice. Please select [1-6]."
                  ;;
              esac
              
              if [ "$troubleshoot_choice" != "6" ]; then
                echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                read -p "Press Enter to continue troubleshooting..."
              fi
            done
          fi
        else
          echo -e "\n❌ Invalid choice. Please enter a number between 1 and $line_num, or 0 to return."
          pause
        fi
      fi
      ;;
    13)
      echo -e "\n💻 POD SHELL ACCESS"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      
      # List running pods only
      echo -e "\n🐳 Running Pods:"
      kubectl get pods --all-namespaces --field-selector=status.phase=Running -o custom-columns="NAMESPACE:.metadata.namespace,POD:.metadata.name" --no-headers > /tmp/running_pods.txt
      nl /tmp/running_pods.txt
      
      read -p $'\nEnter the number of the pod to access: ' shell_pod_choice
      selected_shell_line=$(sed -n "${shell_pod_choice}p" /tmp/running_pods.txt)
      shell_namespace=$(echo $selected_shell_line | awk '{print $1}')
      shell_pod=$(echo $selected_shell_line | awk '{print $2}')
      
      # Get containers in the pod
      shell_containers=$(kubectl get pod "$shell_pod" -n "$shell_namespace" -o jsonpath='{.spec.containers[*].name}')
      shell_container_array=($shell_containers)
      
      # Check if pod has tools/avm-agent containers (kcshell mode)
      has_tools=$(echo "$shell_containers" | tr ' ' '\n' | grep -c "^tools$" || true)
      has_avm_agent=$(echo "$shell_containers" | tr ' ' '\n' | grep -c "^avm-agent$" || true)
      
      if [ "$has_tools" -gt 0 ] || [ "$has_avm_agent" -gt 0 ]; then
        # kcshell mode - special handling for pods with tools/avm-agent
        echo -e "\n🔧 Pod has special containers detected!"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo -e "\n🎯 kcshell Mode - Select container to access:"
        
        kcshell_options=()
        kcshell_commands=()
        option_num=1
        
        # Main container (exclude tools and avm-agent)
        main_container=$(echo "$shell_containers" | tr ' ' '\n' | grep -v "^avm-agent$" | grep -v "^tools$" | head -1)
        if [ -n "$main_container" ]; then
          kcshell_options+=("Main Container: $main_container")
          kcshell_commands+=("$main_container")
          echo "  $option_num) Main Container: $main_container"
          ((option_num++))
        fi
        
        # Tools container
        if [ "$has_tools" -gt 0 ]; then
          tools_container=$(echo "$shell_containers" | tr ' ' '\n' | grep "^tools$" | head -1)
          kcshell_options+=("Tools Container: $tools_container")
          kcshell_commands+=("$tools_container")
          echo "  $option_num) Tools Container: $tools_container"
          ((option_num++))
        fi
        
        # AVM-agent container
        if [ "$has_avm_agent" -gt 0 ]; then
          avm_container=$(echo "$shell_containers" | tr ' ' '\n' | grep "^avm-agent$" | head -1)
          kcshell_options+=("AVM-Agent Container: $avm_container")
          kcshell_commands+=("$avm_container")
          echo "  $option_num) AVM-Agent Container: $avm_container"
          ((option_num++))
        fi
        
        echo "  $option_num) Manual container selection"
        
        read -p $'\nChoose container [1-'"$option_num"']: ' kcshell_choice
        
        if [ "$kcshell_choice" -eq "$option_num" ] 2>/dev/null; then
          # Manual selection
          echo -e "\n📦 All containers:"
          select shell_container in "${shell_container_array[@]}"; do
            if [ -n "$shell_container" ]; then
              break
            fi
          done
        elif [ "$kcshell_choice" -gt 0 ] 2>/dev/null && [ "$kcshell_choice" -lt "$option_num" ]; then
          shell_container="${kcshell_commands[$((kcshell_choice-1))]}"
          echo -e "\n✅ Selected: $shell_container"
        else
          echo "❌ Invalid choice. Exiting."
          pause
          continue
        fi
      elif [ ${#shell_container_array[@]} -eq 1 ]; then
        shell_container=${shell_container_array[0]}
        echo -e "\n📦 Single container found: $shell_container"
      else
        echo -e "\n📦 Multiple containers found. Select one:"
        select shell_container in "${shell_container_array[@]}"; do
          if [ -n "$shell_container" ]; then
            break
          fi
        done
      fi
      
      # For kcshell mode, default to ksh
      if [ "$has_tools" -gt 0 ] || [ "$has_avm_agent" -gt 0 ]; then
        echo -e "\n🔧 kcshell mode - Using ksh by default"
        shell_choice=3
        read -p "Press Enter to connect with ksh, or type 1 (bash), 2 (sh), 4 (custom): " custom_shell_choice
        if [ -n "$custom_shell_choice" ]; then
          shell_choice=$custom_shell_choice
        fi
      else
        echo -e "\n🔧 Select shell to use:"
        echo "1) bash"
        echo "2) sh"
        echo "3) ksh"
        echo "4) Custom command"
        read -p "Choose [1-4]: " shell_choice
      fi
      
      case $shell_choice in
        1)
          echo -e "\n🔍 Finding bash location in pod..."
          shell_path=$(kubectl exec "$shell_pod" -n "$shell_namespace" -c "$shell_container" -- sh -c "which bash 2>/dev/null || command -v bash 2>/dev/null || echo '/bin/bash'" | tr -d '\r')
          echo -e "📍 Using shell: $shell_path"
          echo -e "\n🚀 Connecting to pod with bash... (type 'exit' to return)"
          kubectl exec -it "$shell_pod" -n "$shell_namespace" -c "$shell_container" -- $shell_path
          ;;
        2)
          echo -e "\n🔍 Finding sh location in pod..."
          shell_path=$(kubectl exec "$shell_pod" -n "$shell_namespace" -c "$shell_container" -- sh -c "which sh 2>/dev/null || command -v sh 2>/dev/null || echo '/bin/sh'" | tr -d '\r')
          echo -e "📍 Using shell: $shell_path"
          echo -e "\n🚀 Connecting to pod with sh... (type 'exit' to return)"
          kubectl exec -it "$shell_pod" -n "$shell_namespace" -c "$shell_container" -- $shell_path
          ;;
        3)
          echo -e "\n🔍 Finding ksh location in pod..."
          shell_path=$(kubectl exec "$shell_pod" -n "$shell_namespace" -c "$shell_container" -- sh -c "which ksh 2>/dev/null || command -v ksh 2>/dev/null || echo '/bin/ksh'" | tr -d '\r')
          if kubectl exec "$shell_pod" -n "$shell_namespace" -c "$shell_container" -- test -f "$shell_path" 2>/dev/null; then
            echo -e "📍 Using shell: $shell_path"
            echo -e "\n🚀 Connecting to pod with ksh... (type 'exit' to return)"
            kubectl exec -it "$shell_pod" -n "$shell_namespace" -c "$shell_container" -- $shell_path
          else
            echo -e "❌ ksh not found in pod. Falling back to sh..."
            shell_path=$(kubectl exec "$shell_pod" -n "$shell_namespace" -c "$shell_container" -- sh -c "which sh 2>/dev/null || echo '/bin/sh'" | tr -d '\r')
            kubectl exec -it "$shell_pod" -n "$shell_namespace" -c "$shell_container" -- $shell_path
          fi
          ;;
        4)
          read -p "Enter custom command: " custom_cmd
          kubectl exec -it "$shell_pod" -n "$shell_namespace" -c "$shell_container" -- $custom_cmd
          ;;
        *)
          echo -e "\n🔍 Finding sh location in pod..."
          shell_path=$(kubectl exec "$shell_pod" -n "$shell_namespace" -c "$shell_container" -- sh -c "which sh 2>/dev/null || command -v sh 2>/dev/null || echo '/bin/sh'" | tr -d '\r')
          echo -e "📍 Using shell: $shell_path"
          echo -e "\n🚀 Connecting to pod with sh... (type 'exit' to return)"
          kubectl exec -it "$shell_pod" -n "$shell_namespace" -c "$shell_container" -- $shell_path
          ;;
      esac
      pause
      ;;
    14)
      echo "Exiting. 🚩 J S R!"
      break
      ;;
    *)
      echo "❌ Invalid choice. Please select a valid option [1-14]."
      pause
      ;;
  esac

done
